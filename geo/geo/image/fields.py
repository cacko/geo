from peewee import CharField
from enum import StrEnum


class Source(StrEnum):
    PHOTO = "photo"
    PANORAMA = "panorama"


class SourceField(CharField):
    def db_value(self, value: Source):
        return value.value

    def python_value(self, value):
        return Source(value)
