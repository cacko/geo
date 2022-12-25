from app import create_app
import os
from waitress import serve
from paste.translogger import TransLogger


this_files_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_files_dir)

serve(
    TransLogger(create_app().wsgi_app),
    host=os.environ.get("GEO_BIND_HOST", "0.0.0.0"),
    port=int(os.environ.get("GEO_BIND_PORT", 21234)),
)
