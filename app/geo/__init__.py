from pprint import pprint
import socket
import click
from flask import Blueprint, jsonify, request, abort, current_app
from requests import head
from app.geo.maxmind import MaxMind
import validators
import ipaddress
import socket
from pathlib import Path
from .lookup_image import LookupImage

bp = Blueprint("geo", __name__, url_prefix="/api")


def get_remote_ip(req_ip, forward_ip=None):
    ipv4 = ipaddress.IPv4Address(req_ip)

    if forward_ip:
        return forward_ip

    if ipv4.is_private:
        return socket.gethostbyname(socket.gethostname())
    return req_ip


@bp.cli.command("lookup")
@click.argument("ip")
def cli_full(ip: str):
    pprint(MaxMind.lookup(ip))


@bp.route("/background/<path:place>")
def route_background(place: str):
    try:
        web_assets = Path(current_app.config.get("WEB_BACKGROUNDS"))
        if not web_assets.exists():
            web_assets.mkdir("777", parents=True)
        image = LookupImage(name=place)
        image_path = image.path
        assert image_path.exists()  # type: ignore
        web_path = web_assets / image_path.name
        if not web_path.exists():
            web_path.write_bytes(image_path.read_bytes())
        return jsonify({"name": web_path.name})  # type: ignore
    except AssertionError:
        abort(502)


@bp.route("/lookup")
def route_lookup():
    try:
        ip = request.args.get("ip")
        if not ip:
            ip = get_remote_ip(
                request.remote_addr, request.headers.get("x-forwarded-for")
            )
        assert validators.ip_address.ipv4(ip)  # type: ignore
        return jsonify(MaxMind.lookup(ip).to_dict())  # type: ignore
    except AssertionError:
        abort(502)


@bp.after_request
def after_request(response):
    headers = response.headers
    headers["Access-Control-Allow-Origin"] = "*"
    headers[
        "Access-Control-Allow-Headers"
    ] = "device-id,device-token,Cache-control,Pragma"
    return response
