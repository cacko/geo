import uvicorn
from .config import app_config
import sys

if len(sys.argv) == 1:

    server_config = uvicorn.Config(
        app="app.main:app",
        host=app_config.server.host,
        port=app_config.server.port,
        workers=app_config.server.workers,
        factory=True
    )
    server = uvicorn.Server(server_config)
    server.run()
else:
    import app.cli
    app.cli.run()
