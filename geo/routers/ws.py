from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from geo.geo.image.api import ImageApi
from geo.geo.lookup_image import LookupImage
from geo.config import app_config
from pydantic import BaseModel
from enum import StrEnum
from geo.geo.maxmind import MaxMind
import validators
from geo.core.ip import get_remote_ip


class WSCommand(StrEnum):
    IP = "ip"
    PING = "ping"
    LOOKUP = "lookup"
    BACKGROUND = "background"
    STYLES = "styles"


class Message(BaseModel):
    command: WSCommand
    content: list[str]


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
                content=[
                    get_remote_ip(
                        websocket.headers.get("cf-connecting-ip", websocket.client.host)
                    )
                ],
            ).model_dump()
        )
        await websocket.send_json(
            Message(command=WSCommand.STYLES, content=ImageApi.styles).model_dump()
        )

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def process_command(self, msg: Message):
        try:
            match msg.commmand:
                case WSCommand.LOOKUP:
                    ip = msg.content
                    assert validators.ip_address.ipv4(ip)
                    return MaxMind.lookup(ip).model_dump()
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
                await websocket.send_json(respponse)
            except AssertionError:
                raise HTTPException(400)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
