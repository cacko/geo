from typing import Optional

from geo.geo.image.db import Database
from geo.geo.image.fields import SourceField


from .base import DbModel
from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    BooleanField,
    IntegrityError,
    ManyToManyField,
    BigIntegerField
)

import datetime



class Lookup(DbModel):
    hash = CharField()
    style = CharField()
    ts = BigIntegerField()
    name = CharField()
    url = CharField()
    raw_url = CharField()
    source = SourceField
    last_modified = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def get_or_create(cls, **kwargs) -> tuple['Lookup', bool]:
        defaults = kwargs.pop('defaults', {})
        query = cls.select()
        slug = cls.get_slug(**kwargs)
        query = query.where(cls.slug == slug)

        try:
            return query.get(), False
        except cls.DoesNotExist:
            try:
                if defaults:
                    kwargs.update(defaults)
                with cls._meta.database.atomic():
                    return cls.create(**kwargs), True
            except IntegrityError as exc:
                try:
                    return query.get(), False
                except cls.DoesNotExist:
                    raise exc

    def delete_instance(self, recursive=False, delete_nullable=False):
        self.deleted = True
        self.last_modified = datetime.datetime.now(tz=datetime.timezone.utc)
        self.save(only=["deleted", "last_modified"])

    def save(self, *args, **kwds):
        if not self.slug:
            self.slug = self.__class__.get_slug(**dict(
                Company=self.Company,
                Position=self.Position,
                url=self.url
            ))
        if 'only' not in kwds:
            self.last_modified = datetime.datetime.now(tz=datetime.timezone.utc)
        return super().save(*args, **kwds)


    class Meta:
        database = Database.db
        table_name = 'geo_lookup'
        order_by = ["-last_modified"]
        indexes = (
            (('hash', 'style', 'ts'), True),
        )

