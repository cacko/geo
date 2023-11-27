import logging
import pprint
from typing import Optional
from geo.geo.models import GeoLocation
from .meta import BaseGeoCode
from geopy.geocoders import TomTom
from geo.config import app_config
from pydantic import BaseModel
from enum import StrEnum


class ResultType(StrEnum):
    GEOGRAPHY = "Geography"
    STREET = "Street"
    ADDRESS_RANGE = "Address Range"


class TomTomAddress(BaseModel):
    country: str
    localName: Optional[str] = None
    postalCode: Optional[str] = None
    countrySubdivisionName: Optional[str] = None
    countrySecondarySubdivision: Optional[str] = None
    freeformAddress: Optional[str] = None
    municipality: Optional[str] = None
    streetName: Optional[str] = None


class Point(BaseModel):
    lat: float
    lon: float


class TomTomResult(BaseModel):
    address: TomTomAddress
    position: Point
    type: ResultType
    entityType: Optional[str] = None

    @property
    def name(self):
        if self.entityType:
            return getattr(self.address, self.entityType.lower())
        match self.type:
            case ResultType.STREET:
                return self.address.streetName
            case ResultType.ADDRESS_RANGE:
                return self.address.localName
            case _:
                return ""


class TomTomReverseResult(BaseModel):
    address: TomTomAddress
    position: str

    @property
    def location(self):
        parts = self.position.split(",")
        return [float(x) for x in parts[:2]]

    @property
    def name(self):
        return self.address.localName


class GeoTomTom(BaseGeoCode):

    def __init__(self) -> None:
        self.__coder = TomTom(api_key=app_config.geopy.tomtom_api_key)

    def get_geocode(self, name: str) -> GeoLocation:
        res = self.__coder.geocode(name, language="en-US")
        assert res
        logging.debug(pprint.pformat(res.raw))
        res = TomTomResult(**res.raw)
        return self.__to_model(res)

    def get_reverse(self, lat: float, lon: float) -> GeoLocation:
        res = self.__coder.reverse((lat, lon))
        assert res
        logging.debug(pprint.pformat(res.raw))
        res = TomTomReverseResult(**res.raw)
        return self.__to_model_from_reverse(res)

    def __to_model_from_reverse(self, res: TomTomReverseResult):
        res = GeoLocation(
            country=res.address.country,
            country_iso=self.__class__.country_iso_code(res.address.country),
            city=res.name,
            name=next(filter(None, [res.address.streetName, res.address.municipality]), None),
            subdivions=list(filter(None, [res.address.countrySubdivisionName, res.address.countrySecondarySubdivision])),
            postCode=res.address.postalCode,
            addressLine=res.address.freeformAddress,
            location=res.location
        )
        return res

    def __to_model(self, res: TomTomResult):
        res = GeoLocation(
            country=res.address.country,
            country_iso=self.__class__.country_iso_code(res.address.country),
            city=res.name,
            name=next(filter(None, [res.address.streetName, res.address.municipality]), None),
            subdivions=list(filter(None, [res.address.countrySubdivisionName, res.address.countrySecondarySubdivision])),
            postCode=res.address.postalCode,
            addressLine=res.address.freeformAddress,
            location=[res.position.lat, res.position.lon]
        )
        return res
