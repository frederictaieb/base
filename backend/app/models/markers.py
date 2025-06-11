from pydantic import BaseModel
from typing import List

class Localisation(BaseModel):
    lat: float
    lng: float

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
    localisation: Localisation
    emotions: Emotions
    wisdom: Wisdom
    

# Base de données en mémoire
markers: List[dict] = [
    {
        "localisation":{
            "lat":48.8566, 
            "lng": 2.3522
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
