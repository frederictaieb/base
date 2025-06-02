from pydantic import BaseModel
from typing import List

class Point(BaseModel):
    lat: float
    lng: float

# Base de données en mémoire
points: List[dict] = [
    {"lat": 48.8566, "lng": 2.3522},  # Paris
    {"lat": 40.7128, "lng": -74.0060} # New York
]
