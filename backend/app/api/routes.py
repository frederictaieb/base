from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File, FastAPI
from fastapi.responses import JSONResponse

from app.models.markers import markers, Marker
from app.services.markers_services import markersManager
from app.services.analysis_services import to_phrases, to_summary, to_wisdom, txt_to_emo

from pydantic import BaseModel
from typing import Dict, List



import logging
from app.config.logging_config import setup_logging

from transformers import pipeline

class TextInput(BaseModel):
    text: str

setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter()

class InputData(BaseModel):
    phrases: List[str]

class OutputData(BaseModel):
    summary: str

class WisdomResponse(BaseModel):
    wisdom: List[str]

class EmotionScore(BaseModel):
    label: str
    score: float

class PhraseEmotions(BaseModel):
    emotions: List[EmotionScore]

class EmoResponse(BaseModel):
    summary: str
    wisdom: List[str]
    emotions: List[PhraseEmotions] 

# Take a file
# Return a list of lines
@router.post("/to_phrases")
async def to_phrases_endpoint(file: UploadFile = File(...)):
    return await to_phrases(file)

# Take a list of lines
# Return a summary
@router.post("/to_summary", response_model=OutputData)
async def to_summarize_endpoint(data: InputData):
    return await to_summary(data)

# Take a list of lines
# Return wisdom
@router.post("/to_wisdom", response_model=WisdomResponse)
async def to_wisdom_endpoint(data: InputData):
    return await to_wisdom(data)

@router.post("/txt_to_emo", response_model=EmoResponse)
async def txt_to_emo_endpoint(file: UploadFile = File(...)):
    return await txt_to_emo(file)

 

 

@router.get("/markers")
def get_markers():
    return markers

@router.post("/add_marker")
async def add_marker(marker: Marker):
    markers.append(marker.dict())
    await markersManager.broadcast(marker.dict())
    return {"status": "ok"}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await markersManager.connect(websocket)
    try:
        await websocket.send_json({"type": "init", 'markers': markers})
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        markersManager.disconnect(websocket)
