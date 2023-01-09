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
    subdivisions: Optional[str]
    location: Optional[tuple[float, float]]
    timezone: Optional[str]
    ISP: Optional[ASNInfo]


class CityInfo(BaseModel):
    country: str
    country_iso: str
    city: str
    ip: str
    subdivisions: Optional[str]
    location: Optional[tuple[float, float]]
    timezone: Optional[str]