from pprint import pprint
import click
from flask import Blueprint, jsonify, request
from app.geo.maxmind import MaxMind


bp = Blueprint("geo", __name__, url_prefix="/geo")


@bp.cli.command("lookup")
@click.argument("ip")
def cli_full(ip: str):
    pprint(MaxMind.lookup(ip))



@bp.cli.command("asn")
@click.argument("ip")
def cli_full(ip: str):
    pprint(MaxMind.asn(ip))



@bp.route("/")
def route_index():
    ip = request.args.get("ip")
    return jsonify(MaxMind.lookup(ip).to_dict())
