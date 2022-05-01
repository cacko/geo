from pprint import pprint
from socket import socket
import click
from flask import Blueprint, jsonify, request
from app.geo.maxmind import MaxMind
import validators
import ipaddress
import socket

bp = Blueprint("geo", __name__, url_prefix="/geo")


def get_remote_ip(req_ip):
    ipv4 = ipaddress.IPv4Address(req_ip)
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
    if not ip or not validators.ip_address.ipv4(ip):
        ip = get_remote_ip(request.remote_addr)
    return jsonify(MaxMind.lookup(ip).to_dict())
