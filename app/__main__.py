import uvicorn
from .config import app_config
import logging
import sys

if len(sys.argv) == 1:
    uvicorn.run(
        "app.main:app",
        host=app_config.server.host,
        port=app_config.server.port,
        reload=app_config.server.reload,
        workers=app_config.server.workers
    )
else:
    import app.cli
    app.cli.run()
