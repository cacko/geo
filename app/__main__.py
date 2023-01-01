import uvicorn
from .config import app_config
import logging

uvicorn.run(
    "app.main:app", 
    host=app_config.server.host, 
    port=app_config.server.port,
    log_level=getattr(logging, app_config.log.level),
    reload=app_config.server.reload
)