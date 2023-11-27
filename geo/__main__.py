from .config import app_config
from geo.main import app
import sys
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

if len(sys.argv) == 1:

    server_config = Config.from_mapping(
        bind=f"{app_config.server.host}:{app_config.server.port}",
        worker_class="trio"
    )
    asyncio.run(serve(app, server_config))
else:
    from geo.cli import run
    run()
