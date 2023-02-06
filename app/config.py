from pydantic import BaseModel, BaseSettings, Field


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


class ServerConfig(BaseModel):
    host: str
    port: int
    reload: bool = Field(default=False)
    workers: int = Field(default=1)


class LogConfig(BaseModel):
    level: str = Field(default="INFO")


class WebConfig(BaseModel):
    backgrounds: str
    backgrounds_path: str


class StorageConfig(BaseModel):
    dir: str


class FlickrConfig(BaseModel):
    key: str
    secret: str


class Settings(BaseSettings):
    redis: RedisConfig
    maxmind: MaxmindConfig
    server: ServerConfig
    log: LogConfig
    web: WebConfig
    storage: StorageConfig
    flickr: FlickrConfig

    class Config:
        env_nested_delimiter = '__'


app_config = Settings() # type: ignore
