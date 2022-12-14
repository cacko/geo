from cachable import Cachable
from cachable.storage import RedisStorage
from dataclasses_json import dataclass_json
from dataclasses import dataclass
from pathlib import Path
from enum import Enum
from geoip2.database import Reader
from geoip2.models import City, ASN
from validators import ip_address
from flask import Flask
from stringcase import snakecase
from typing import Optional


@dataclass_json()
@dataclass()
class Config:
    db: str


class DatabaseType(Enum):
    CITY = "GeoIP2-City.mmdb"
    CITY_LITE = "GeoLite2-City.mmdb"
    ASN = "GeoLite2-ASN.mmdb"


class GeoDbMeta(type):

    __db: Optional[Path] = None
    __instances: dict[DatabaseType, "GeoDb"] = {}

    def __call__(cls, db: DatabaseType, *args, **kwargs):
        if db not in cls.__instances:
            assert cls.__db
            db_path = Path(cls.__db) / db.value
            cls.__instances[db] = type.__call__(cls, db_path, *args, **kwargs)
        return cls.__instances[db]

    def register(cls, app: "Flask", cfg: dict):
        config = Config.from_dict(cfg)  # type: ignore
        cls.__db = Path(app.instance_path) / config.db

    def city(cls, ip) -> City:
        return CityDb(ip).lookup()

    def city_lite(cls, ip) -> City:
        return CityLiteDb(ip).lookup()

    def asn(cls, ip) -> ASN:
        return ASNDb(ip).lookup()


class GeoDb(object, metaclass=GeoDbMeta):

    __db: Reader

    def __init__(self, db_path: Path) -> None:
        self.__db = Reader(db_path.as_posix())

    def do_city(self, ip: str):
        if not ip_address.ipv4(ip):
            raise ValueError
        return self.__db.city(ip)

    def do_asn(self, ip: str):
        if all([not ip_address.ipv4(ip), not ip_address.ipv4_cidr(ip)]):
            raise ValueError
        return self.__db.asn(ip)


class CityDb(Cachable):

    _ip: str

    def __init__(self, ip: str) -> None:
        super().__init__()
        self._ip = ip

    @property
    def storage(self):
        return RedisStorage

    @property
    def id(self):
        return snakecase(self._ip)

    def lookup(self) -> City:
        if not self.load():
            self._struct = GeoDb(DatabaseType.CITY).do_city(self._ip)
            if self._struct:
                self.tocache(self._struct)
        return self._struct


class CityLiteDb(CityDb):
    def lookup(self) -> City:
        if not self.load():
            self._struct = GeoDb(DatabaseType.CITY_LITE).do_city(self._ip)
            if self._struct:
                self.tocache(self._struct)
        return self._struct


class ASNDb(Cachable):

    __ip: str

    def __init__(self, ip: str) -> None:
        super().__init__()
        self.__ip = ip

    @property
    def storage(self):
        return RedisStorage

    @property
    def id(self):
        return snakecase(self.__ip)

    def lookup(self) -> City:
        if not self.load():
            self._struct = GeoDb(DatabaseType.ASN).do_asn(self.__ip)
            if self._struct:
                self.tocache(self._struct)
        return self._struct
