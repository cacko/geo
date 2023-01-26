from cachable.storage.filestorage.image import CachableFileImage
from cachable.storage import FileStorage
from corestring import string_hash
from typing import Optional
from cachable.request import Request, Method, BinaryStruct
from app.flickr import Flickr
import filetype
import logging
from PIL import Image
from io import BytesIO
from app.geo.models import GeoInfo
from pydantic import BaseModel, Field
from app.config import app_config
from pathlib import Path
from uuid import uuid4
from corefile import TempPath


class LookupImageParams(BaseModel):
    prompt: Optional[str] = None
    height: int = Field(default=512)
    width: int = Field(default=768)
    guidance_scale: float = Field(default=15)
    num_inference_steps: int = Field(default=50)
    seed: Optional[int] = None
    model: str = Field(default="oj2")
    upscale: bool = Field(default=True)


class LookupImage(CachableFileImage):

    _geo: GeoInfo

    def __init__(self, geo: Optional[GeoInfo] = None):
        self._geo = geo

    def tocache(self, image_data: bytes):
        assert self._path
        im = Image.open(BytesIO(image_data))
        im.save(self._path.as_posix())

    def post_init(self):
        self._path = Path(app_config.web.backgrounds) / f"{self.store_key}"

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
        return f"{hash}.webp"

    @property
    def prompt(self) -> str:
        return (
            "classical oil painting by marc simonetti, "
            "stylistic, brush strokes, oil, canvas, 8k, hdr"
        )

    @property
    def tags(self) -> str:
        return ",".join(filter(None, ["town", self._geo.city, self._geo.country]))

    def _init(self):
        if self.isCached:
            return
        try:
            self.__fetch(LookupImageParams(prompt=self.prompt).dict())
        except Exception:
            self._path = self.DEFAULT

    def __fetch(self, json: dict):
        rand_id = uuid4().hex
        flick_path = TempPath(f"{rand_id}.png")
        gps = ",".join(map(str,self._geo.location))
        path = f"http://192.168.0.107:23726/image/gps2img/{gps}"
        params = LookupImageParams(
            num_inference_steps=25,
        )
        req = Request(
            path,
            method=Method.POST,
            data=params.dict(),
        )
        is_multipart = req.is_multipart
        if is_multipart:
            multipart = req.multipart
            for part in multipart.parts:
                content_type = part.headers.get(
                    b"content-type", b""  # type: ignore
                ).decode()
                if content_type.startswith("image"):
                    flick_path.write_bytes(part.content)


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
