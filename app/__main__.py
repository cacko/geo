import uvicorn
from .config import app_config
from app.main import app
import sys
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

if len(sys.argv) == 1:

    server_config = Config.from_mapping(
        bind=f"{app_config.server.host}:{app_config.server.port}",
        # workers=app_config.server.workers,
        worker_class="trio"
    )
    server = uvicorn.Server(server_config)
    asyncio.run(serve(app, server_config))
else:
    import app.cli
    app.cli.run()
