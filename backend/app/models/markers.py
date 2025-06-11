from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    latitude: float
    longitude: float

class Emotions(BaseModel):
    joy: int
    sadness: int
    anger: int
    fear: int

class Wisdom(BaseModel):
   sentence_1 : str
   sentence_2 : str
   sentence_3 : str

class Marker(BaseModel):
    location: Location
    emotions: Emotions
    wisdom: Wisdom
    

# Base de données en mémoire
markers: List[dict] = [
    {
        "location":{
            "latitude":40.7128, 
            "longitude": -74.0060
            }, 
        "emotions":{
            "joy": 10, 
            "sadness": 0, 
            "anger": 0, 
            "fear": 0
            }, 
        "wisdom":{
            "sentence_1":"La nuit c'est les étoile qui parlent", 
            "sentence_2":"Le chocolat, c'est la vie", 
            "sentence_3":"Le sucre c'est pas top"
            }
    }
]
