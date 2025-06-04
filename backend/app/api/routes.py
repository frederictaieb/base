from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.markers import markers, Marker
from app.services.markers_services import markersManager

router = APIRouter()

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
