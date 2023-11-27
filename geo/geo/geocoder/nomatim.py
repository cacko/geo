import pprint
import logging
from typing import Optional
from geo.geo.models import GeoLocation
from .meta import BaseGeoCode
from geopy.geocoders import Nominatim
from pydantic import BaseModel


class NomatumAddress(BaseModel):
    country: str
    city: str
    postcode: Optional[str] = None
    state: Optional[str] = None
    suburb: Optional[str] = None
    road: Optional[str] = None


class Point(BaseModel):
    coordinates: list[float]
    type: str


class NomatumResult(BaseModel):
    address: NomatumAddress
    extratags: dict[str, str]
    display_name: str
    name: str
    lat: float
    lon: float


class GeoNomatim(BaseGeoCode):

    def __init__(self) -> None:
        self.__coder = Nominatim(user_agent="geo.cacko.net py/3.11")

    def get_geocode(self, name: str) -> GeoLocation:
        res = self.__coder.geocode(name, addressdetails=True, extratags=True)
        assert res
        logging.debug(pprint.pformat(res.raw))
        res = NomatumResult(**res.raw)
        return self.__to_model(res)

    def get_reverse(self, lat: float, lon: float) -> GeoLocation:
        res = self.__coder.reverse((lat, lon))
        assert res
        logging.debug(pprint.pformat(res.raw))
        res = NomatumResult(**res.raw)
        return self.__to_model(res)

    def __to_model(self, res: NomatumResult):
        res = GeoLocation(
            country=res.address.country,
            country_iso=self.__class__.country_iso_code(res.address.country),
            city=res.address.city,
            name=res.display_name,
            subdivions=list(filter(None, [res.address.state, res.address.suburb])),
            postCode=res.address.postcode,
            addressLine=res.name,
            location=[res.lat, res.lon],
            extra=res.extratags
        )
        return res
