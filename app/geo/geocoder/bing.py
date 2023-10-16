import pprint
from typing import Optional
from app.geo.models import GeoLocation
from .meta import BaseGeoCode
from geopy.geocoders import Bing
from app.config import app_config
from pydantic import BaseModel


class BingAddress(BaseModel):
    countryRegion: str
    formattedAddress: str
    locality: str
    postalCode: Optional[str] = None
    adminDistrict: Optional[str] = None
    adminDistrict2: Optional[str] = None
    addressLine: Optional[str] = None


class BingPoint(BaseModel):
    coordinates: list[float]
    type: str


class BingResult(BaseModel):
    address: BingAddress
    name: str
    point: BingPoint


class GeoBing(BaseGeoCode):

    def __init__(self) -> None:
        self.__coder = Bing(api_key=app_config.geopy.bing_api_key)

    def get_geocode(self, name: str) -> GeoLocation:
        res = self.__coder(name)
        assert res
        res = BingResult(**res.raw)
        return self.__to_model(res)

    def get_reverse(self, lat: float, lon: float) -> GeoLocation:
        res = self.__coder.reverse((lat, lon))
        assert res
        pprint.pprint(res.raw)
        res = BingResult(**res.raw)
        return self.__to_model(res)

    def __to_model(self, res: BingResult):
        res = GeoLocation(
            country=res.address.countryRegion,
            country_iso=self.__class__.country_iso_code(res.address.countryRegion),
            city=res.address.locality,
            name=res.address.formattedAddress,
            subdivions=[res.address.adminDistrict, res.address.adminDistrict2],
            postCode=res.address.postalCode,
            addressLine=res.address.addressLine,
            location=res.point.coordinates
        )
        return res
