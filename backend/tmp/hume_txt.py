from transformers import pipeline

classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
result = classifier("I feel amazing today!")
print(result)

classifier = pipeline("audio-classification", model="superb/hubert-large-superb-er")
result = classifier("path/to/your_audio.wav")
print(result)