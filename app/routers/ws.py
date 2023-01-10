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

    ips: dict[str, str] = {}

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        conn_ip = websocket.headers.get("x-forwarded-for")
        old_ip = self.ips.get(client_id, "")
        if old_ip != conn_ip:
            self.ips[client_id] = conn_ip
            await websocket.send_json(
                Message(
                    source="ip", content=conn_ip
                ).dict()
            )

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket, client_id: str):
        logging.warning(f">>>>> {client_id}")
        conn_ip = websocket.headers.get("x-forwarded-for")
        old_ip = self.ips.get(client_id, "")
        if old_ip != conn_ip:
            self.ips[client_id] = conn_ip
            await websocket.send_json(
                Message(
                    source="ip", content=conn_ip
                ).dict()
            )
        logging.debug(f"{websocket.headers.get('x-forwarded-for')}")
        await websocket.send_json(Message(source="ws", content=f"{message}").dict())


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket, client_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
