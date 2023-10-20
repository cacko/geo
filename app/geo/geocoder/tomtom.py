import logging
import pprint
from typing import Optional
from app.geo.models import GeoLocation
from .meta import BaseGeoCode
from geopy.geocoders import TomTom
from app.config import app_config
from pydantic import BaseModel


class TomTomAddress(BaseModel):
    country: str
    localName: str
    postalCode: Optional[str] = None
    countrySubdivisionName: Optional[str] = None
    countrySecondarySubdivision: Optional[str] = None
    freeformAddress: Optional[str] = None
    municipality: Optional[str] = None
    streetName: Optional[str] = None


class Point(BaseModel):
    lat: float
    lng: float


class TomTomResult(BaseModel):
    address: TomTomAddress
    position: Point


class GeoTomTom(BaseGeoCode):

    def __init__(self) -> None:
        self.__coder = TomTom(api_key=app_config.geopy.tomtom_api_key)

    def get_geocode(self, name: str) -> GeoLocation:
        res = self.__coder.geocode(name, language="en-US")
        assert res
        logging.debug(pprint.pformat(res.raw))
        res = TomTomAddress(**res.raw)
        return self.__to_model(res)

    def get_reverse(self, lat: float, lon: float) -> GeoLocation:
        res = self.__coder.reverse((lat, lon))
        assert res
        logging.debug(pprint.pformat(res.raw))
        res = TomTomResult(**res.raw)
        return self.__to_model(res)

    def __to_model(self, res: TomTomResult):
        res = GeoLocation(
            country=res.address.country,
            country_iso=self.__class__.country_iso_code(res.address.country),
            city=res.address.localName,
            name=next(filter(None, [res.address.streetName, res.address.municipality]), None),
            subdivions=list(filter(None, [res.address.countrySubdivisionName, res.address.countrySecondarySubdivision])),
            postCode=res.address.postalCode,
            addressLine=res.address.freeformAddress,
            location=[res.position.lat, res.position.lng]
        )
        return res
