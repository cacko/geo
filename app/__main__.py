from app import create_app
import os
from waitress import serve
from paste.translogger import TransLogger
import logging

this_files_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_files_dir)

host = os.environ.get("GEO_BIND_HOST", "0.0.0.0")
port = int(os.environ.get("GEO_BIND_PORT", 21234)

logging.info(f"Starting geo app {host}:{port}")

serve(
    TransLogger(create_app().wsgi_app),
    host=host,
    port=port),
)
