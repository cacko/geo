import logging
import time
from cachable.storage.filestorage.image import CachableFileImage
from cachable.storage import FileStorage
from cachable.request import Request
from corestring import string_hash
from corefile import filepath
from typing import Optional
from PIL import Image
from io import BytesIO
from geo.geo.models import GeoInfo, GeoLocation, ImageOptions
from geo.config import app_config
from pathlib import Path
from random import choice


class LookupImageMeta(type):
    
    def __call__(cls, *args, **kwds):
        return type.__call__(cls, *args, **kwds)

    @property
    def styles(cls) -> list[str]:
        res = Request(cls.endpoint(app_config.masha.api_options))
        options = ImageOptions(**res.json)
        return options.styles
    
    def endpoint(cls, path: str) -> str:
        masha_config = app_config.masha
        return f"http://{masha_config.host}:{masha_config.port}/{path}"


class BaseLookupImage(CachableFileImage):
    pass


class LookupImage(BaseLookupImage, metaclass=LookupImageMeta):
    def __init__(
        self,
        geo: Optional[GeoInfo | GeoLocation] = None,
        ts: Optional[int] = None,
        style: Optional[str] = None,
    ):
        self._ts = ts
        self._geo = geo
        self._style = style

    @property
    def style(self) -> str:
        if not self._style:
            self._style = choice(self.styles)
        return self._style

    def tocache(self, image_data: bytes):
        assert self._path
        im = Image.open(BytesIO(image_data))
        im.save(self._path.as_posix())

    def post_init(self):
        self._path = self.cache_path / f"{self.store_key}"

    @property
    def cache_path(self) -> Path:
        return Path(app_config.web.backgrounds)

    @property
    def storage(self):
        return FileStorage

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
        parts = [
            self.__class__.endpoint(app_config.masha.api_gps2img),
            self.style,
            gps
        ]
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
