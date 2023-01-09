
from fastapi import APIRouter, WebSocket
from app.geo.maxmind import MaxMind
import validators
import logging
from app.core.ip import get_remote_ip
from app.geo.lookup_image import LookupImage
from app.config import app_config
import random
from uuid import uuid4

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    await websocket.send_json({
        'conn': uuid4().hex
    });
    while True:
        try:
            # Wait for any message from the client
            message = await websocket.receive_text()
            logging.debug(message)
            # Send message to the client
            resp = {'value': random.uniform(0, 1)}
            await websocket.send_json(resp)
        except Exception as e:
            print('error:', e)
            break
    print('Bye..')