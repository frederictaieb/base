import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import numpy as np
from pydub import AudioSegment

voices = {
    "alain": ["An old man speaks with a neutral tone and natural pace. He is calm, relaxed. The speech is in French. The speech is clear and expressive, recorded in studio quality. There is no accent. there is a 3 seconds silence at the beginning and at the end."],
    "pierre": [""],
    "thomas": [""],
}

def generate_audio(prompt: str, voice: str = "alain") -> bytes:
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # Modèle + tokenizer
    model = ParlerTTSForConditionalGeneration.from_pretrained("PHBJT/french_parler_tts_mini_v0.1").to(device)
    tokenizer = AutoTokenizer.from_pretrained("PHBJT/french_parler_tts_mini_v0.1", use_fast=True)

    # ✅ Description vocale EN ANGLAIS, mais qui précise que la voix parle en français
    description = voices[voice]
    
    input_ids = tokenizer(description, return_tensors="pt", padding=True).input_ids.to(device)
    prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()
    audio_int16 = (audio_arr * 32767).astype(np.int16)
    audio_segment = AudioSegment(
       audio_int16.tobytes(),
       frame_rate=44000,
       sample_width=2,  # 16 bits = 2 bytes
       channels=1
    )
    audio_segment.export("w01.mp3", format="mp3")

    return audio_segment

if __name__ == "__main__":
    generate_audio(f"Ça, t'as raison. Cette ville devient infernale... Moi et ma Madame on vendra cet endroit un jour prochain, je pense. Si on pouvait acheter un gentil petit restaurant en centre-ville ou un relais, ça nous irait.")