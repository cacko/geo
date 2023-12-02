from typing import Optional
from pydantic import BaseModel
from enum import StrEnum


class Choices(object):
    @classmethod
    def values(cls):
        return [m.value for m in cls.__members__.values()]

    @classmethod
    def keys(cls):
        return [m.lower() for m in cls.__members__.keys()]

    @classmethod
    def members(cls):
        return cls.__members__.values()


class ImageStyle(Choices, StrEnum):
    ILLUSTRATION = "illustration"
    PAINTING = "painting"


class ASNInfo(BaseModel):
    name: str
    id: int


class GeoInfo(BaseModel):
    country: str
    country_iso: str
    city: str
    ip: str
    subdivisions: Optional[str] = None
    location: Optional[tuple[float, float]]
    timezone: Optional[str] = None
    addressLine: Optional[str] = None
    postCode: Optional[str] = None
    ISP: Optional[ASNInfo] = None


class CityInfo(BaseModel):
    country: str
    country_iso: str
    city: str
    ip: str
    subdivisions: Optional[str] = None
    location: Optional[tuple[float, float]] = None
    timezone: Optional[str] = None


class GeoLocation(BaseModel):
    country: str
    country_iso: str
    city: str
    name: str
    subdivions: Optional[list[str]] = None
    addressLine: Optional[str] = None
    postCode: Optional[str] = None
    location: Optional[list[float]] = None
    extra: Optional[dict[str, str]] = None


class ImageOptions(BaseModel):
    model: list[str]
    resolution: list[str]
    category: list[str]
    template: list[str]
    qrcode: list[str]
    styles: list[str]
