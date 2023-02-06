from app.config import app_config
import flickrapi
import json
from pathlib import Path
from corefile import TempPath
from cachable.request import Request
from typing import Optional
import logging


class FlickrMeta(type):

    __instance: Optional["Flickr"] = None

    def __call__(cls):
        if not cls.__instance:
            cls.__instance = type.__call__(cls)
        return cls.__instance

    def image(cls, tags: str, lat: float, lon: float) -> Optional[Path]:
        return cls().get_image(tags=tags, lat=lat, lon=lon)


class Flickr(object, metaclass=FlickrMeta):

    __api: flickrapi.FlickrAPI

    def __init__(self) -> None:
        self.__api = flickrapi.FlickrAPI(
            api_key=app_config.flickr.key,
            secret=app_config.flickr.secret,
            format="json",
        )

    def get_image(self, tags: str, lat: float, lon: float) -> Optional[Path]:
        try:
            extras = "url_h"
            response = self.__api.photos.search(
                tags=tags, 
                lat=lat, 
                lon=lon, 
                per_page="1", 
                extras=extras,
                sort='relevance'
            )
            result = json.loads(response)
            assert isinstance(result, dict)
            photos_data = result.get("photos", {})
            photos = photos_data.get("photo", [])
            assert len(photos)
            photo = photos[0]
            url = photo.get("url_h")
            if not url:
                url = f"https://live.staticflickr.com/{photo.get('server')}/{photo.get('id')}_{photo.get('secret')}_b.jpg"
            url_path = Path(url)
            tmp_path = TempPath(f"{__class__.__name__}{url_path.name}")
            req = Request(url=url)
            tmp_path.write_bytes(req.binary.binary)
            return tmp_path
        except AssertionError:
            return None
