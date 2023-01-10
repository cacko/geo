from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
from app.config import app_config
from pydantic import BaseModel
from enum import Enum


class WSCommand(Enum):
    IP = "ip"


class Message(BaseModel):
    command: WSCommand
    content: str


router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await websocket.send_json(
            Message(
                command=WSCommand.IP, 
                content=websocket.headers.get("x-forwarded-for")
            ).dict()
        )

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(Message(source="ws", content=f"{message}").dict())


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
