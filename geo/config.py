from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class MaxmindConfig(BaseModel):
    db: str
    city_db: str
    country_db: str
    asn_db: str
    city2_db: str
    asn2_db: str


class RedisConfig(BaseModel):
    cli: str
    url: str


class MashaConfig(BaseModel):
    host: str
    port: str
    api_gps2img: str


class ServerConfig(BaseModel):
    host: str
    port: int
    reload: bool = Field(default=False)
    workers: int = Field(default=5)


class LogConfig(BaseModel):
    level: str = Field(default="INFO")


class WebConfig(BaseModel):
    backgrounds: str
    backgrounds_path: str


class StorageConfig(BaseModel):
    dir: str


class GeoPyConfig(BaseModel):
    bing_api_key: str
    here_api_key: str
    tomtom_api_key: str


class Settings(BaseSettings):
    redis: RedisConfig
    maxmind: MaxmindConfig
    server: ServerConfig
    log: LogConfig
    web: WebConfig
    storage: StorageConfig
    geopy: GeoPyConfig
    masha: MashaConfig

    class Config:
        env_nested_delimiter = "__"


app_config = Settings()  # type: ignore
