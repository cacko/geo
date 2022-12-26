from cachable.storage.filestorage.image import CachableFileImage
from cachable.storage import FileStorage
from corestring import string_hash
from typing import Optional
from cachable.request import Request, Method, BinaryStruct
from dataclasses import dataclass, field, asdict
import logging


@dataclass
class LookupImageParams:
    prompt: str
    height: int = field(default=512)
    width: int = field(default=768)
    guidance_scale: float = field(default=15)
    seed: Optional[int] = None


class LookupImage(CachableFileImage):

    _name: str
    SIZE = (768, 512)

    def __init__(self, name: str):
        self._name = name

    @property
    def storage(self):
        return FileStorage

    @property
    def filename(self):
        return f"{string_hash(self._name)}.png"

    @property
    def prompt(self) -> str:
        return (
            f"{self._name}, "
            "with  stunning 3d render + dim volumetric lighting, "
            "8k octane beautifully detailed render, post-processing, "
            "extremely hyperdetailed, intricate, ray of sunlight, "
            "detailed painterly digital art style by WLOP and , "
            "8k octane beautifully detailed render, post-processing, "
            "extremely hyperdetailed, intricate, epic composition, "
            "sparkling atmosphere, cinematic lighting + masterpiece, "
            "trending on artstation, very detailed, vibrant colors, "
            "hyperrealistic, smooth, sharp focus, lifelike, "
            "cinematic lighting, art by artgerm and greg rutkowski "
            "and alphonse mucha diffuse lighting, fantasy, intricate, elegant, highly detailed"
        )

    def _init(self):
        if self.isCached:
            return
        try:
            self.__fetch(asdict(LookupImageParams(prompt=self.prompt)))
        except Exception:
            self._path = self.DEFAULT

    def __make_request(self, path: str, json: Optional[dict] = None):
        params = {}

        if json:
            params["json"] = json

        return Request(path, method=Method.POST, **params)

    def __fetch(self, json: dict):
        path = f"http://192.168.0.107:23726/image/txt2img/{self._name}"
        req = self.__make_request(path=path, json=json)
        is_multipart = req.is_multipart
        if is_multipart:
            multipart = req.multipart
            for part in multipart.parts:
                content_type = part.headers.get(
                    b"content-type", b""  # type: ignore
                ).decode()
                logging.warning(f">>>>>>>>>>>> {content_type}")
                if content_type.startswith("image"):
                    logging.warning(f">>>>>>>>>>>>>> {self.storage.storage_path}")
                    self._path.write_bytes(part.content)
        return False
