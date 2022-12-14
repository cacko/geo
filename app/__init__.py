from os import environ
from isoflask import ISOFlask
from cachable.storage.redis import RedisStorage
from cachable.storage.file import FileStorage
from pathlib import Path
import logging
import os
from app.geo.geodb import GeoDb

import structlog
import logging
import os

structlog.configure(
    processors=[
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

formatter = structlog.stdlib.ProcessorFormatter(
    processors=[
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.dev.ConsoleRenderer(),
    ],
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
root_logger = logging.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(getattr(logging, os.environ.get("GEO_LOG_LEVEL", "INFO")))


FileStorage.register(Path(environ.get("STORAGE_DIR", "")))
RedisStorage.register(environ.get("REDIS_URL", ""))


def create_app(test_config=None):

    app = ISOFlask(__name__, instance_relative_config=True)
    app.config.from_envvar("FLASK_CONFIG")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    GeoDb.register(app, app.config.get_namespace("MAXMIND_"))

    from app.geo import bp as geo_bp

    app.register_blueprint(geo_bp)

    return app
