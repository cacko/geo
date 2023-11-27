from cachable.storage.filestorage.image import CachableFileImage
from cachable.storage import FileStorage
from cachable.request import Request, Method
from corestring import string_hash
from typing import Optional
from PIL import Image
from io import BytesIO
from app.geo.models import GeoInfo
from pydantic import BaseModel, Field
from app.config import app_config
from pathlib import Path


class LookupImageParams(BaseModel):
    prompt: Optional[str] = None
    height: int = Field(default=576)
    width: int = Field(default=1024)
    guidance_scale: float = Field(default=11)
    num_inference_steps: int = Field(default=20)
    seed: Optional[int] = None
    model: Optional[str] = None
    upscale: bool = Field(default=True)


class LookupImage(CachableFileImage):
    def __init__(self, geo: Optional[GeoInfo] = None, ts: Optional[int] = None):
        self._ts = ts
        self._geo = geo

    def tocache(self, image_data: bytes):
        assert self._path
        im = Image.open(BytesIO(image_data))
        im.save(self._path.as_posix())
        if self._ts:
            nots_path = self._path.as_posix().replace(f"{self._ts}.webp", ".webp")
            im.save(nots_path)

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
        ts = f"{self._ts}" if self._ts else ""
        return f"{hash}{ts}.webp"

    @property
    def prompt(self) -> str:
        return (
            "<lora:lcm_lora_weights:1>,cinematic,vibrant colors,realistic, hdr, 8k"
        )

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
    def gps2img_endpoint(self) -> str:
        masha_config = app_config.masha
        return (
            f"http://{masha_config.host}:{masha_config.port}/{masha_config.api_gps2img}"
        )

    def __fetch(self):
        assert self._geo
        assert self._geo.location
        gps = ",".join(map(str, self._geo.location))
        path = f"{self.gps2img_endpoint}/{gps}"
        params = LookupImageParams(prompt=self.prompt)
        req = Request(
            path,
            method=Method.POST,
            data=params.model_dump(),
        )
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
