
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
from app.config import app_config
import random
from uuid import uuid4

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     print('Accepting client connection...')
#     await websocket.accept()
#     await websocket.send_json({
#         'conn': uuid4().hex
#     });
#     while True:
#         try:
#             # Wait for any message from the client
#             message = await websocket.receive_text()
#             websocket.client.r
#             logging.debug(message)
#             # Send message to the client
#             resp = {'value': random.uniform(0, 1)}
#             await websocket.send_json(resp)
#         except Exception as e:
#             print('error:', e)
#             break
#     print('Bye..')