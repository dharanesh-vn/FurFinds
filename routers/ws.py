from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from realtime import manager

router = APIRouter(tags=["realtime"])


@router.websocket("/ws")
async def websocket_updates(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive; client messages are optional.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
