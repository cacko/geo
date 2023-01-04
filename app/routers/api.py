from fastapi import APIRouter, Header, Request, HTTPException
from app.geo.maxmind import MaxMind
import validators
import logging
from app.core.ip import get_remote_ip

router = APIRouter()


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
