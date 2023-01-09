from pathlib import Path
from geoip2.models import City, ASN
from typing import Optional, Any
import logging

class GeoDbMeta(type):

    __db_root: Optional[Path] = None
    __instances: dict[str, Any] = {}

    def __call__(cls, *args, **kwargs):
        k = cls.__name__
        if k not in cls.__instances:
            cls.__instances[k] = type.__call__(cls, *args, **kwargs)
        return cls.__instances[k]

    def register(cls, db_path: Path):
        cls.__db_root = db_path

    @property
    def db_root(cls) -> Path:
        return cls.__db_root

    def city(cls, ip) -> City:
        return cls().do_city(ip)

    def asn(cls, ip) -> ASN:
        return cls().do_asn(ip)


