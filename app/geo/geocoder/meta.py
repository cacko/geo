

from typing import Any
from pycountry import countries
from app.geo.models import GeoLocation


class GeoCoderMeta(type):

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        return type.__call__(cls, *args, **kwds)

    def from_name(cls, name: str) -> GeoLocation:
        return cls().get_geocode(name)

    def from_gps(cls, lat: float, lon: float) -> GeoLocation:
        return cls().get_reverse(lat, lon)

    def country_iso_code(cls, name: str) -> str:
        res = countries.search_fuzzy(name)
        return res.pop(0).alpha_2


class BaseGeoCode(object, metaclass=GeoCoderMeta):

    def get_geocode(self, name: str) -> GeoLocation:
        raise NotImplementedError

    def get_reverse(self, lat: float, lon: float) -> GeoLocation:
        raise NotImplementedError
