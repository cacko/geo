from cachable import Cachable
from cachable.storage import RedisStorage
from geoip2.database import Reader
from geo.geo.models import CityInfo, ASNInfo
from validators import ip_address
from stringcase import snakecase
from geo.config import app_config
from .meta import GeoDbMeta


class CityIP(Cachable):

    _ip: str

    def __init__(self, ip: str):
        self._ip = ip

    @property
    def storage(self):
        return RedisStorage

    @property
    def id(self):
        return snakecase(self._ip)


class ASNIP(Cachable):

    __ip: str

    def __init__(self, ip: str):
        self.__ip = ip

    @property
    def storage(self):
        return RedisStorage

    @property
    def id(self):
        return snakecase(self.__ip)


class GeoDb(object, metaclass=GeoDbMeta):

    __city_db: Reader
    __asn_db: Reader

    def __init__(self) -> None:
        pth = __class__.db_root / app_config.maxmind.city2_db
        pth_asn = __class__.db_root / app_config.maxmind.asn2_db
        self.__city_db = Reader(pth.as_posix())
        self.__asn_db = Reader(pth_asn.as_posix())

    def do_city(self, ip: str) -> CityInfo:
        if not ip_address.ipv4(ip):
            raise ValueError
        cache = CityIP(ip)
        if cache.load():
            return cache._struct

        res = self.__city_db.city(ip)
        return cache.tocache(CityInfo(
            ip=ip,
            country=res.country.names.get("en", ""),
            country_iso=res.country.iso_code,
            city=res.city.names.get("en", ""),
            subdivisions=",".join([s.names.get("en") for s in res.subdivisions]),
            location=(res.location.latitude, res.location.longitude),
            timezone=res.location.time_zone
        ))

    def do_asn(self, ip: str) -> ASNInfo:
        if all([not ip_address.ipv4(ip), not ip_address.ipv4(ip, cidr=True)]):
            raise ValueError
        cache = ASNIP(ip)
        if cache.load():
            return cache._struct
        res = self.__asn_db.asn(ip)
        return cache.tocache(ASNInfo(
            name=res.autonomous_system_organization,
            id=res.autonomous_system_number
        ))
