from os import name
from typing import Optional
from fastapi import APIRouter, HTTPException
from geo.core import IPError
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
    except IPError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get("/api/address/{address:path}", tags=["api"])
def read_address(address: str, coder: Coders = Coders.HERE):
    try:
        return coder.coder.from_name(address).model_dump()
    except AssertionError:
        raise HTTPException(status_code=404)


@router.get("/api/gps/{lat}/{lon}", tags=["api"])
def read_gps(lat: float, lon: float, coder: Coders = Coders.HERE):
    try:
        return coder.coder.from_gps(lat, lon).model_dump()
    except AssertionError:
        raise HTTPException(status_code=404)


@router.get("/api/streetview/{ip_gps}/{ts}", tags=["api"])
@router.get("/api/streetview/{ip_gps}", tags=["api"])
def route_streetview(
    ip_gps: str, 
    ts: Optional[int] = None, 
    style: str = None
):
    try:
        logging.info(ip_gps)
        geo_info = None
        if gps := PATTERN_GPS.search(ip_gps):
            lat, lng = map(float, gps.groups())
            geo_info = Coders.HERE.coder.from_gps(lat, lng)
        else:
            geo_info = MaxMind.lookup(ip=ip_gps)
        image = LookupImage(geo=geo_info, ts=ts, style=style)
        image_path = image.path
        assert image_path
        assert image_path.exists()
        return {
            "name": image.metadata.name,
            "url": image.metadata.url,
            "style": image.style,
            "raw_url": image.metadata.raw_url
        }
    except AssertionError:
        raise HTTPException(status_code=502)
