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
from geo.geo.models import GeoInfo, ImageOptions
from geo.config import app_config
from pathlib import Path
from random import choice


class LookupImage(CachableFileImage):
    def __init__(self, geo: Optional[GeoInfo] = None, ts: Optional[int] = None):
        self._ts = ts
        self._geo = geo

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
                ts = fp.stem.split(".")[-1].replace(hash, "")
                logging.debug(f"ts={ts}")
        return f"{hash}{ts}.webp"

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

    @property
    def styles(self) -> list[str]:
        res = Request(self.__endpoint(app_config.masha.api_options))
        options = ImageOptions(**res.json)
        return options.styles

    def __endpoint(self, path: str) -> str:
        masha_config = app_config.masha
        return f"http://{masha_config.host}:{masha_config.port}/{path}"

    def __fetch(self):
        assert self._geo
        assert self._geo.location
        gps = ",".join(map(str, self._geo.location))
        style = choice(self.styles)
        path = f"{self.__endpoint(app_config.masha.api_gps2img)}/{style}/{gps}"
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