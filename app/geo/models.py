from typing import Optional
from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class ASNInfo:
    name: str
    id: int


@dataclass_json
@dataclass
class GeoInfo:
    country: str
    city: str
    ip: str
    subdivisions: Optional[list[str]]
    location: Optional[tuple[float, float]]
    timezone: Optional[str]
    ISP: Optional[ASNInfo]
