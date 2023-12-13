
from typing import Optional
from cachable.request import Request
from geo.config import app_config
from geo.geo.models import ImageOptions


class ImageApiMeta(type):
    
    __instance: Optional['ImageApiMeta'] = None
    
    def __call__(cls, *args, **kwds):
        if not cls.__instance:
            cls.__instance = type.__call__(cls, *args, **kwds)
        return cls.__instance
    
    @property
    def styles(cls) -> list[str]:
        return cls().get_styles()
    
    def endpoint(cls, path: str) -> str:
        return cls().get_endpoint(path)


class ImageApi(object, metaclass=ImageApiMeta):
    

    def get_styles(self) -> list[str]:
        res = Request(self.get_endpoint(app_config.masha.api_options))
        options = ImageOptions(**res.json)
        return options.styles
    
    def get_endpoint(cls, path: str) -> str:
        masha_config = app_config.masha
        return f"http://{masha_config.host}:{masha_config.port}/{path}"

