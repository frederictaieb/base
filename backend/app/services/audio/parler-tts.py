import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

voices = {
    "alain": ["An old man speaks with a neutral tone and natural pace. He is calm, relaxed and talks slowly. The speech is clear and expressive, recorded in studio quality. The speech is in French. There is no accent. there is a pause at beginning and end. Add some vintage noise The speech is in French. There is no accent. there is a pause at beginning and end."],
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
    return audio_arr

if __name__ == "__main__":
    audio_arr = generate_audio("Bonjour et bienvenue dans cette démonstration de synthèse.")
    sf.write("parler_tts_fr.wav", audio_arr, 16000)