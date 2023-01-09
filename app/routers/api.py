from fastapi import APIRouter, Header, Request, HTTPException
from app.geo.maxmind import MaxMind
import validators
import logging
from app.core.ip import get_remote_ip
from app.geo.lookup_image import LookupImage
from app.config import app_config

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
        return MaxMind.lookup(ip).dict()
    except AssertionError:
        raise HTTPException(status_code=502)


@router.get("/api/background/{ip}", tags=["api"])
async def route_background(ip: str):
    try:
        logging.warning(ip)
        geo_info = MaxMind.lookup(ip=ip)
        image = LookupImage(geo=geo_info)
        image_path = image.path
        assert image_path
        assert image_path.exists()
        return {
            "name": image_path.name,
            "url": f"{app_config.web.backgrounds_path}/{image_path.name}",
        }
    except AssertionError:
        raise HTTPException(status_code=502)
