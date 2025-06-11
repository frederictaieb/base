from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    latitude: float
    longitude: float

class Marker(BaseModel):
    location: Location
    
# Base de données en mémoire
markers: List[dict] = [
    {
        "location":{
            "latitude":40.7128, 
            "longitude": -74.0060
        }
    }
]
