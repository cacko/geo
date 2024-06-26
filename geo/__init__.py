from cachable.storage.redis import RedisStorage
from cachable.storage.file import FileStorage
from pathlib import Path
from .geo.maxmind import MaxMind
from .config import app_config
import corelog
__name__ = "geo"

corelog.register(app_config.log.level)

FileStorage.register(Path(app_config.storage.dir))
RedisStorage.register(app_config.redis.url)
MaxMind.register(app_config.maxmind.db)
