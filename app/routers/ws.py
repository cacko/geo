from fastapi import (
    APIRouter, WebSocket, WebSocketDisconnect, HTTPException
)
from app.geo.lookup_image import LookupImage
import logging
from app.config import app_config
from pydantic import BaseModel
from enum import Enum
from app.geo.maxmind import MaxMind
import validators

class WSCommand(Enum):
    IP = "ip"
    PING = "ping"
    LOOKUP = "lookup"
    BACKGROUND = "background"


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

    async def process_command(self, msg: Message):
        try:
            match msg.commmand:
                case WSCommand.LOOKUP:
                    ip = msg.content
                    assert validators.ip_address.ipv4(ip)
                    return MaxMind.lookup(ip).dict()
                case WSCommand.BACKGROUND:
                    geo_info = MaxMind.lookup(ip=ip)
                    image = LookupImage(geo=geo_info)
                    image_path = image.path
                    assert image_path
                    assert image_path.exists()
                    return {
                        "name": image_path.name,
                        "url": f"{app_config.web.backgrounds_path}/{image_path.name}",
                    }
                case WSCommand.PING:
                    pass
                case _:
                    pass
        except AssertionError:
            raise HTTPException(400)

    # async def send_personal_message(self, message: str, websocket: WebSocket):
    #     await websocket.send_json(Message(source="ws", content=f"{message}").dict())


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            try:
                data = await websocket.receive_text()
                assert isinstance(data, Message)
                respponse = await manager.process_command(data)
                websocket.send_json(respponse)
            except AssertionError:
                raise HTTPException(400)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
