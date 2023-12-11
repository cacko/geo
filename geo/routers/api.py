from typing import Optional
from fastapi import APIRouter, HTTPException
from geo.geo.maxmind import MaxMind
from geo.geo.geocoder import Coders
import validators
import logging
from geo.geo.lookup_image import LookupImage
from geo.config import app_config
from geo.geo.models import GeoInfo
from geo.core.ip import get_ip_from_input
import re

PATTERN_GPS = re.compile(r"(-?\d+\.\d+)[,\s]+(-?\d+\.\d+)")

router = APIRouter()


@router.get("/api/ip/{ip}", tags=["api"])
def read_ip(
    ip: str,
):
    try:
        ip = get_ip_from_input(ip)
        res = MaxMind.lookup(ip)
        if res.location:
            coder_res = Coders.HERE.coder.from_gps(*res.location)
            res = GeoInfo(**{**res.model_dump(), **coder_res.model_dump()})
        return res.model_dump()
    except AssertionError as e:
        raise HTTPException(status_code=404, detail=e.__str__)



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


@router.get("/api/background/{ip}/{ts}", tags=["api"])
@router.get("/api/background/{ip}", tags=["api"])
def route_background(
    ip: str,
    ts: Optional[int] = None
):
    try:
        logging.info(ip)
        geo_info = None
        if gps := PATTERN_GPS.search(ip):
            lat, lng = map(float, gps.groups())
            geo_info = Coders.HERE.coder.from_gps(lat, lng)
        else:
            geo_info = MaxMind.lookup(ip=ip)
        image = LookupImage(geo=geo_info, ts=ts)
        image_path = image.path
        assert image_path
        assert image_path.exists()
        return {
            "name": image_path.name,
            "url": f"{app_config.web.backgrounds_path}/{image_path.name}",
        }
    except AssertionError:
        raise HTTPException(status_code=502)
