from dataclasses_json import dataclass_json
from dataclasses import dataclass
from pathlib import Path
from app.geo.geodb import GeoDb
from app.geo.models import ASNInfo, GeoInfo


@dataclass_json()
@dataclass()
class Config:
    db: str


class MaxMindMeta(type):

    __db: Path = None
    __instance: 'MaxMind' = None

    def __call__(cls,  *args, **kwargs):
        if not cls.__instance:
            cls.__instance = type.__call__(cls, *args, **kwargs)
        return cls.__instance

    def register(cls, app, config: dict):
        config: Config = Config.from_dict(config)
        cls.__db = Path(config.db)

    @property
    def db(cls) -> Path:
        return cls.__db

    def lookup(cls, ip: str) -> GeoInfo:
        return cls().get_info(ip)

    def asn(cls, ip: str):
        return cls().get_asn(ip)


class MaxMind(object, metaclass=MaxMindMeta):

    def get_info(self, ip: str):
        city = GeoDb.city(ip)
        if not city:
            return None
        return GeoInfo(
            ip=ip,
            country=city.country.names['en'] if city.country else 'N/A',
            city=city.city.names['en'] if city.city else 'N/A',
            subdivisions=[s.names['en'] for s in city.subdivisions],
            location=(city.location.latitude, city.location.longitude),
            timezone=city.location.time_zone,
            ISP=self.get_asn(ip)

        )

    def get_asn(self, ip: str) -> ASNInfo:
        res = GeoDb.asn(ip)
        if not res:
            return None
        return ASNInfo(
            name=res.autonomous_system_organization,
            id=res.autonomous_system_number
        )
