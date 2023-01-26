from cachable import Cachable
from cachable.storage import RedisStorage
from validators import ip_address
from stringcase import snakecase
from typing import Optional
from app.config import app_config
import logging
import GeoIP
from .meta import GeoDbMeta
from app.geo.models import ASNInfo, CityInfo


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
    def __init__(self) -> None:
        pth = __class__.db_root / app_config.maxmind.city_db
        pth_asn = __class__.db_root / app_config.maxmind.asn_db
        self.__city_db = GeoIP.open(pth.as_posix(), GeoIP.GEOIP_STANDARD)
        self.__asn_db = GeoIP.open(pth_asn.as_posix(), GeoIP.GEOIP_STANDARD)

    def do_city(self, ip: str) -> CityInfo:
        if not ip_address.ipv4(ip):
            raise ValueError
        cache = CityIP(ip)
        logging.warning(cache)
        logging.warning(cache.isCached)
        if cache.load():
            return cache._struct
        res = self.__city_db.record_by_addr(ip)
        res = dict(filter(lambda x: x[1], res.items()))
        return cache.tocache(CityInfo(
            ip=ip,
            country=res.get("country_name", ""),
            country_iso=res.get("country_code", ""),
            city=res.get("city", ""),
            subdivisions=res.get("region_name", ""),
            location=(res["longitude"], res["latitude"]),
            timezone=res.get("time_zone", "")
        ))

    def do_asn(self, ip: str):
        try:
            assert not ll([not ip_address.ipv4(ip), not ip_address.ipv4_cidr(ip)])
            cache = ASNIP(ip)
            if cache.load():
                return cache._struct
            res = self.__asn_db.org_by_addr(ip)
            assert res
            asid, name = res.split(" ", 1)
            return ASNInfo(
                name= name,
                id=int(asid.lstrip("AS"))
            )
        except AssertionError as e:
            logging.exception(e)
            raise ValueError

