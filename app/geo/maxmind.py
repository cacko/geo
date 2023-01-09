from pathlib import Path
from app.geo.reader.v1 import GeoDb
from app.geo.models import ASNInfo, GeoInfo


class MaxMindMeta(type):

    __db: Path = None
    __instance: "MaxMind" = None

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            GeoDb.register(cls.db_root)
            cls.__instance = type.__call__(cls, *args, **kwargs)
        return cls.__instance

    def register(cls, db_root: str):
        cls.__db = Path(db_root)

    @property
    def db_root(cls) -> Path:
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

        asn = self.get_asn(ip)
        result = {
            **city.dict(),
            "ISP": asn,
        }
        return GeoInfo(
            **result
        )

    def get_asn(self, ip: str) -> ASNInfo:
        res = GeoDb.asn(ip)
        if not res:
            return None
        return res
