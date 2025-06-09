from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File, FastAPI
from fastapi.responses import JSONResponse

from app.models.markers import markers, Marker
from app.services.markers_services import markersManager
from app.services.analysis_services import textfile_to_emo, textfile_to_summary, textfile_to_wisdom, textfile_to_emotions, textfile_to_heatmap

from pydantic import BaseModel
from typing import Dict, List

from fastapi.responses import StreamingResponse

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

# Take a list of lines
# Return a summary
@router.post("/text_to_summary", response_model=OutputData)
async def textfile_to_summary_endpoint(file: UploadFile = File(...)):
    return await textfile_to_summary(file)

# Take a list of lines
# Return wisdom
@router.post("/text_to_wisdom", response_model=WisdomResponse)
async def textfile_to_wisdom_endpoint(file: UploadFile = File(...)):
    return await textfile_to_wisdom(file)

# Take a list of lines
# Return a heatmap
@router.post("/textfile_to_heatmap")
async def textfile_to_heatmap_endpoint(file: UploadFile = File(...)):
    buffer = await textfile_to_heatmap(file)
    return StreamingResponse(buffer, media_type="image/png")

# Take a file
# Return emotionnal analysis, including summary, wisdom, emotions and heatmap
@router.post("/textfile_to_emo", response_model=EmoResponse)
async def textfile_to_emo_endpoint(file: UploadFile = File(...)):
    return await textfile_to_emo(file)

 
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
