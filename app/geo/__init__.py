from pprint import pprint
import click
from flask import Blueprint, jsonify, request
from app.geo.maxmind import MaxMind
import socket


bp = Blueprint("geo", __name__, url_prefix="/geo")


@bp.cli.command("lookup")
@click.argument("ip")
def cli_full(ip: str):
    pprint(MaxMind.lookup(ip))


@bp.route("/")
def route_index():
    print(request.remote_addr)
    ip = request.args.get("ip", socket.gethostbyname(socket.gethostname()))
    return jsonify(MaxMind.lookup(ip).to_dict())
