from pathlib import Path
from geo.geo.reader.v1 import GeoDb
from geo.geo.models import ASNInfo, GeoInfo
from typing import Optional


class MaxMindMeta(type):

    __db: Optional[Path] = None
    __instance: Optional["MaxMind"] = None

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            GeoDb.register(cls.db_root)
            cls.__instance = type.__call__(cls, *args, **kwargs)
        return cls.__instance

    def register(cls, db_root: str):
        cls.__db = Path(db_root)

    @property
    def db_root(cls) -> Path:
        assert cls.__db
        return cls.__db

    def lookup(cls, ip: str) -> Optional[GeoInfo]:
        return cls().get_info(ip)

    def asn(cls, ip: str) -> Optional[ASNInfo]:
        return cls().get_asn(ip)


class MaxMind(object, metaclass=MaxMindMeta):
    def get_info(self, ip: str) -> Optional[GeoInfo]:
        try:
            city = GeoDb.city(ip)
            assert city
            asn = self.get_asn(ip)
            result = {
                **city.dict(),
                "ISP": asn,
            }
            return GeoInfo(**result)
        except AssertionError:
            return None

    def get_asn(self, ip: str) -> Optional[ASNInfo]:
        res = GeoDb.asn(ip)
        if not res:
            return None
        return res
