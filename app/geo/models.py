from typing import Optional
from pydantic import BaseModel


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
