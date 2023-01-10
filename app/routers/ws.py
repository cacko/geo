from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
from app.config import app_config
import random
from uuid import uuid4
from pydantic import BaseModel


class Message(BaseModel):
    source: str
    content: str


router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        headers = [f"{k}={v}" for k,v in websocket.headers.items()]
        await websocket.send_json(
            Message(source="ws", content=" ".join(headers)).dict()
        )

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(
            Message(source="ws", content=f"hi {websocket.client.host}").dict()
        )

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
