from fastapi import APIRouter, HTTPException
from app.geo.maxmind import MaxMind
from app.geo.geocoder import Coders
import validators
import logging
from app.geo.lookup_image import LookupImage
from app.config import app_config
from app.geo.models import GeoInfo

router = APIRouter()


@router.get("/api/ip/{ip}", tags=["api"])
def read_lookup(
    ip: str,
):
    try:
        assert validators.ip_address.ipv4(ip)
        res = MaxMind.lookup(ip)
        if res.location:
            coder_res = Coders.HERE.coder.from_gps(*res.location)
            res = GeoInfo(**{**res.model_dump(), **coder_res.model_dump()})
        return res.model_dump()
    except AssertionError:
        raise HTTPException(status_code=404)


@router.get("/api/address/{address:path}", tags=["api"])
def read_address(
    address: str,
    coder: Coders = Coders.HERE
):
    try:
        return coder.coder.from_name(address).model_dump()
    except AssertionError:
        raise HTTPException(status_code=404)


@router.get("/api/gps/{lat}/{lon}", tags=["api"])
def read_gps(
    lat: float,
    lon: float,
    coder: Coders = Coders.HERE

):
    try:
        return coder.coder.from_gps(lat, lon).model_dump()
    except AssertionError:
        raise HTTPException(status_code=404)


@router.get("/api/background/{ip}", tags=["api"])
def route_background(
    ip: str,
    renew: bool = False
):
    try:
        logging.warning(ip)
        geo_info = MaxMind.lookup(ip=ip)
        image = LookupImage(geo=geo_info, renew=renew)
        image_path = image.path
        assert image_path
        assert image_path.exists()
        return {
            "name": image_path.name,
            "url": f"{app_config.web.backgrounds_path}/{image_path.name}",
        }
    except AssertionError:
        raise HTTPException(status_code=502)
