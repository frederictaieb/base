from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.point import points, Point
from app.services.manager import manager

router = APIRouter()

@router.get("/points")
def get_points():
    return points

@router.post("/add_point")
async def add_point(point: Point):
    points.append(point.dict())
    await manager.broadcast(point.dict())
    return {"status": "ok"}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_json({"type": "init", "points": points})
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
