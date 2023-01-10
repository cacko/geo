from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
from app.config import app_config
import random
from uuid import uuid4
from pydantic import BaseModel


class Connection(BaseModel, arbitrary_types_allowed=True):
    id: str
    ws: WebSocket
    ip: str


class Message(BaseModel):
    source: str
    content: str


router = APIRouter()


class ConnectionManager:

    active_connections: dict[str, Connection] = {}

    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        old_ip = ""
        if client_id in self.active_connections:
            old_ip = self.active_connections[client_id].ip
            self.active_connections[client_id].ws.close()
        await websocket.accept()
        conn_ip = websocket.headers.get("x-forwarded-for")
        self.active_connections[client_id] = Connection(
            id=client_id,
            ws=websocket,
            ip=conn_ip
        )
        if old_ip != conn_ip:
            self.active_connections[client_id].ip = conn_ip
            await websocket.send_json(Message(source="ip", content=conn_ip).dict())

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: Message, websocket: WebSocket):
        await websocket.send_json(message.dict())


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # conn_ip = websocket.headers.get("x-forwarded-for")
            # old_ip = manager.ips.get(client_id, "")
            # logging.warning(f">>>>> {client_id} {conn_ip} {old_ip}")
            # if old_ip != conn_ip:
            #     await manager.send_message(
            #         Message(source="ip", content=conn_ip), websocket
            #     )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
