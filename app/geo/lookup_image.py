from cachable.storage.filestorage.image import CachableFileImage
from cachable.storage import FileStorage
from corestring import string_hash
from typing import Optional
from cachable.request import Request, Method, BinaryStruct
from dataclasses import dataclass, field, asdict
from app.flickr import Flickr
import filetype
import logging
from PIL import Image
from io import BytesIO
from app.geo.models import GeoInfo


@dataclass
class LookupImageParams:
    prompt: str
    height: int = field(default=512)
    width: int = field(default=768)
    guidance_scale: float = field(default=15)
    seed: Optional[int] = None


class LookupImage(CachableFileImage):

    _geo: GeoInfo

    def __init__(self, geo: Optional[GeoInfo] = None):
        self._geo = geo

    def tocache(self, res: BinaryStruct):
        assert self._path
        im = Image.open(BytesIO(res.binary))
        im.save(self._path.as_posix())

    def post_init(self):
        self._path = self.storage.storage_path / f"{self.store_key}"

    @property
    def storage(self):
        return FileStorage

    @property
    def name(self) -> str:
        return " ".join(filter(None, [
            self._geo.country, self._geo.city, ",".join(map(str, self._geo.location))
        ]))

    @property
    def filename(self):
        hash = string_hash(
            self._geo.country, self._geo.city, ",".join(map(str, self._geo.location))
        )
        return f"{hash}.png"

    @property
    def prompt(self) -> str:
        return (
            "with  stunning 3d render + dim volumetric lighting, "
            "8k octane beautifully detailed render, post-processing, "
            "extremely hyperdetailed, intricate, ray of sunlight, "
            "detailed painterly digital art style by WLOP and , "
            "sparkling atmosphere, cinematic lighting + masterpiece, "
            "trending on artstation, very detailed, vibrant colors, "
            "hyperrealistic, smooth, sharp focus, lifelike, "
            "cinematic lighting, art by artgerm and greg rutkowski "
            "and alphonse mucha diffuse lighting, fantasy, intricate, elegant, highly detailed"
        )

    @property
    def tags(self) -> list[str]:
        return list(filter(None, [self._geo.country, self._geo.city, "town"]))

    def _init(self):
        if self.isCached:
            return
        try:
            self.__fetch(asdict(LookupImageParams(prompt=self.prompt)))
        except Exception:
            self._path = self.DEFAULT

    def __make_request(self, path: str, **kwds):
        logging.warning(kwds)
        return Request(path, method=Method.POST, **kwds)

    def __fetch(self, json: dict):
        flick_path = Flickr.image(
            tags=self.tags, lat=self._geo.location[0], lon=self._geo.location[1]
        )
        logging.warning(flick_path.exists())
        kind = filetype.guess(flick_path.as_posix())
        fp = flick_path.open("rb")
        path = f"http://192.168.0.107:23726/image/img2img/{self.name}"
        req = Request(
            path,
            method=Method.POST,
            data=json,
            files={"file": (f"{flick_path.name}", fp, kind.mime, {"Expires": "0"})},
        )
        is_multipart = req.is_multipart
        if is_multipart:
            multipart = req.multipart
            for part in multipart.parts:
                content_type = part.headers.get(
                    b"content-type", b""  # type: ignore
                ).decode()
                if content_type.startswith("image"):
                    self._path.write_bytes(part.content)
        return False


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
