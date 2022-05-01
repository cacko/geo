from cachable import Cachable
from os import environ
from flask import Flask
from flask.json import JSONEncoder
import logging
import os
from app.geo.geodb import GeoDb

Cachable.register(
    redis_url=environ.get("REDIS_URL"),
    storage_dir=environ.get("STORAGE_DIR")
)


class ISOFlask(Flask):
    json_encoder = JSONEncoder


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_envvar("FLASK_CONFIG")
    if app.debug or os.environ.get("FLASK_RUN_FROM_CLI", None):
        app.logger.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "INFO")))
    else:
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    GeoDb.register(app, app.config.get_namespace("MAXMIND_"))

    from app.geo import bp as geo_bp

    app.register_blueprint(geo_bp)

    return app
