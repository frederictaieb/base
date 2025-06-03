from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.inner_weather import inner_weathers, InnerWeather
from app.services.makers_services import markers_emitter

router = APIRouter()

@router.get("/inner_weathers")
def get_inner_weathers():
    return inner_weathers

@router.post("/add_inner_weather")
async def add_inner_weather(inner_weather: InnerWeather):
    inner_weathers.append(inner_weather.dict())
    await markers_emitter.broadcast(inner_weather.dict())
    return {"status": "ok"}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await markers_emitter.connect(websocket)
    try:
        await websocket.send_json({"type": "init", "inner_weathers": inner_weathers})
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        markers_emitter.disconnect(websocket)
