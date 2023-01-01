from fastapi import APIRouter, Header, Request, HTTPException
from app.geo.maxmind import MaxMind
from app.geo.lookup_image import LookupImage
import ipaddress
import validators
import socket
import httpx
import logging

router = APIRouter()


def get_remote_ip(req_ip, forward_ip=None):
    try:
        ipv4 = ipaddress.IPv4Address(req_ip)
        if forward_ip:
            return forward_ip
        if ipv4.is_private:
            return httpx.get("https://checkip.amazonaws.com").text.strip()
    except socket.gaierror:
        pass
    return req_ip


@router.get("/api/lookup", tags=["api"])
async def read_lookup(
    request: Request,
    ip: str = "",
    x_forwarded_for: str | None = Header(default=None),
):
    try:
        if not ip:
            ip = get_remote_ip(request.client.host, x_forwarded_for)
        assert validators.ip_address.ipv4(ip)
        return MaxMind.lookup(ip).to_dict()
    except AssertionError:
        raise HTTPException(status_code=502)


@router.get("/api/background/{place}", tags=["api"])
async def read_background(place: str):
    try:
        image = LookupImage(name=place)
        image_path = image.path
        assert image_path
        assert image_path.exists()
        return {"name": image_path.name}
    except AssertionError:
        raise HTTPException(status_code=502)
