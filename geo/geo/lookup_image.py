import json
import logging
import time
from cachable.storage.filestorage.image import CachableFileImage
from cachable.storage import FileStorage
from cachable.request import Request
from corestring import string_hash
from corefile import filepath
from typing import Optional
from PIL import Image
from PIL.ExifTags import Base as TagNames
from io import BytesIO

from pydantic import BaseModel
from geo.geo.models import GeoInfo, GeoLocation, ImageOptions
from geo.config import app_config
from pathlib import Path
from random import choice
from geo.geo.image.api import ImageApi


class LookupMetadata(BaseModel):
    url: str
    raw_url: str
    name: str


class LookupImage(CachableFileImage):
    def __init__(
        self,
        geo: Optional[GeoInfo | GeoLocation] = None,
        ts: Optional[int] = None,
        style: Optional[str] = None,
    ):
        self._ts = ts
        self._geo = geo
        self._style = style
        self._metadata = {}

    @property
    def style(self) -> str:
        if not self._style:
            self._style = choice(ImageApi.styles)
        return self._style

    def tocache(self, image_data: bytes):
        assert self._path

    def post_init(self):
        self._path = self.cache_path / f"{self.store_key}"

    @property
    def cache_path(self) -> Path:
        return Path(app_config.web.backgrounds)

    @property
    def storage(self):
        return FileStorage

    @property
    def metadata(self):
        if "raw_url" not in self._metadata:
            with Image.open(self.path) as img:
                ex = img.getexif()
                self._metadata["raw_url"] = ex[TagNames.DocumentName]
        return self._metadata

    @property
    def name(self) -> str:
        return " ".join(
            filter(
                None,
                [
                    self._geo.country,
                    self._geo.city,
                    ",".join(map(str, self._geo.location)),
                ],
            )
        )

    @property
    def filename(self):
        hash = string_hash(
            self._geo.country, self._geo.city, ",".join(map(str, self._geo.location))
        )
        try:
            assert self._ts
            ts = f"{self._ts}"
            logging.debug(f"getting filename {hash} ts={ts}")
        except AssertionError:
            ts = f"{int(time.time())}"
            prefix = f"{self.__class__.__name__}.{hash}"
            logging.debug(f"searching in {self.cache_path} with {prefix}")
            found = list(filepath(root=self.cache_path, prefix=prefix))
            if len(found):
                fp = choice(found)
                logging.debug(f"found {fp}")
                stem_parts = fp.stem.split(".")
                ts = stem_parts.pop()
                style = stem_parts.pop()
                if not self._style:
                    self._style = style
        return f"{hash}.{self.style}.{ts}.webp"

    @property
    def isCached(self) -> bool:
        trd = super().isCached
        logging.warning(f"{self._path} -> {self._path.exists()}")
        return trd

    @property
    def tags(self) -> str:
        return ",".join(filter(None, ["town", self._geo.city, self._geo.country]))

    def _init(self):
        if self.isCached:
            return
        try:
            self.__fetch()
        except Exception:
            self._path = self.DEFAULT

    def __fetch(self):
        assert self._geo
        assert self._geo.location
        gps = ",".join(map(str, self._geo.location))
        parts = [ImageApi.endpoint(app_config.masha.api_gps2img), self.style, gps]
        path = "/".join(parts)
        req = Request(path)
        is_multipart = req.is_multipart
        if is_multipart:
            multipart = req.multipart
            for part in multipart.parts:
                content_type = part.headers.get(
                    b"content-type", b""  # type: ignore
                ).decode()
                if content_type.startswith("image"):
                    assert self._path
                    self._path.write_bytes(part.content)
                else:
                    self._metadata = LookupMetadata(**json.loads(part.content))
        else:
            logging.info(req.body)
            try:
                self._metadata  = LookupMetadata(**json.loads(req.body))
            except json.JSONDecodeError as e:
                logging.exception(e)
        logging.info(self._path)
        logging.info(self._metadata)
        self._path.write_text(self._metadata.url)


class LoadingImage(LookupImage):
    def __init__(self, name: str):
        super().__init__(name)

    @property
    def isCached(self) -> bool:
        return False

    @property
    def store_key(self):
        return self.filename

    @property
    def filename(self):
        return "loading.png"
