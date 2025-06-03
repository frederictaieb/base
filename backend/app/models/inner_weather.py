from pydantic import BaseModel
from typing import List

class EmotionScore(BaseModel):
    joy: int
    sadness: int
    anger: int
    fear: int

class Point(BaseModel):
    lat: float
    lng: float

class Sentences(BaseModel):
   sentences: List[str]

class InnerWeather(BaseModel):
    point: Point
    sentences: Sentences
    emotion_score: EmotionScore

# Base de données en mémoire
inner_weathers: List[dict] = [
    {"point": {"lat": 48.8566, "lng": 2.3522}, "sentences": ["La nuit c'est les étoile qui parlent", "Le chocolat, c'est la vie", "Le sucre c'est pas top"], "emotion_score": {"joy": 10, "sadness": 0, "anger": 0, "fear": 0}},  # Paris
    {"point": {"lat": 40.7128, "lng": -74.0060}, "sentences": ["oui, c'est comme ca que ca commence", "et pas comme ca que ca termine", "nuit et jours les chats sont la"], "emotion_score": {"joy": 10, "sadness": 0, "anger": 0, "fear": 0}} # New York
]
