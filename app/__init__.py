from cachable.storage.redis import RedisStorage
from cachable.storage.file import FileStorage
from pathlib import Path
from .geo.geodb import GeoDb
from .config import app_config
import corelog

corelog.register(app_config.log.level)

FileStorage.register(Path(app_config.storage.dir))
RedisStorage.register(app_config.redis.url)
GeoDb.register(Path(app_config.maxmind.db))
