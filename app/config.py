from pydantic import BaseModel, BaseSettings, Field

class MaxmindConfig(BaseModel):
    db: str

class RedisConfig(BaseModel):
    cli: str
    url: str

class ServerConfig(BaseModel):
    host: str
    port: int
    reload: bool = Field(default=False)


class LogConfig(BaseModel):
    level: str = Field(default="INFO")

class WebConfig(BaseModel):
    backgrounds: str

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


app_config = Settings()