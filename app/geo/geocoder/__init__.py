from .meta import GeoCoderMeta
from .bing import GeoBing
from .nomatim import GeoNomatim
from .here import GeoHere
from enum import StrEnum


class Coders(StrEnum):
    BING = "bing"
    NOMATUM = "nomatum"
    HERE = "here"

    @classmethod
    def _missing_(cls, value):
        return Coders.HERE

    @property
    def coder(self) -> GeoCoderMeta:
        match self:
            case Coders.BING:
                return GeoBing
            case Coders.NOMATUM:
                return GeoNomatim
            case Coders.HERE:
                return GeoHere
            case _:
                raise NotImplementedError


__all__ = ["Coders", "GeoBing", "GeoNomatim"]
