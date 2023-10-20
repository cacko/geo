import logging
import pprint
from typing import Optional
from app.geo.models import GeoLocation
from .meta import BaseGeoCode
from geopy.geocoders import HereV7
from app.config import app_config
from pydantic import BaseModel


class HereAddress(BaseModel):
    countryName: str
    label: str
    city: str
    postalCode: Optional[str] = None
    county: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    street: Optional[str] = None


class Position(BaseModel):
    lat: float
    lng: float


class HereResult(BaseModel):
    address: HereAddress
    title: str
    position: Position


class GeoHere(BaseGeoCode):

    def __init__(self) -> None:
        self.__coder = HereV7(apikey=app_config.geopy.here_api_key)

    def get_geocode(self, name: str) -> GeoLocation:
        res = self.__coder.geocode(name, language="en-US")
        assert res
        logging.debug(pprint.pformat(res.raw))
        res = HereResult(**res.raw)
        return self.__to_model(res)

    def get_reverse(self, lat: float, lon: float) -> GeoLocation:
        res = self.__coder.reverse((lat, lon), language="en-US")
        assert res
        logging.debug(pprint.pformat(res.raw))
        res = HereResult(**res.raw)
        return self.__to_model(res)

    def __to_model(self, res: HereResult):
        res = GeoLocation(
            country=res.address.countryName,
            country_iso=self.__class__.country_iso_code(res.address.countryName),
            city=res.address.city,
            name=res.address.label,
            subdivions=list(filter(None, [res.address.state, res.address.county, res.address.district])),
            postCode=res.address.postalCode,
            addressLine=res.title,
            location=[res.position.lat, res.position.lng]
        )
        return res
