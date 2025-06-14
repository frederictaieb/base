from gtts import gTTS
import os

def text_to_speech(text: str, lang: str = "fr", filename: str = "output.mp3"):
    try:
        # Générer le speech
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        print(f"✅ Fichier audio généré : {filename}")

        # Lire le fichier audio (si tu es sur macOS / Linux)
        os.system(f"open {filename}")  # macOS
        # os.system(f"xdg-open {filename}")  # Linux
        # os.startfile(filename)  # Windows

    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    text = "ceci est un test"
    text_to_speech(text)