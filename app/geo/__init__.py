from pprint import pprint
import socket
import click
from flask import Blueprint, jsonify, request
from requests import head
from app.geo.maxmind import MaxMind
import validators
import ipaddress
import socket

bp = Blueprint("geo", __name__, url_prefix="/geo")


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


@bp.route("/")
def route_index():
    ip = request.args.get("ip")
    assert ip
    if not validators.ip_address.ipv4(ip):  # type: ignore
        ip = get_remote_ip(request.remote_addr, request.headers.get("x-forwarded-for"))
    return jsonify(MaxMind.lookup(ip).to_dict())  # type: ignore
