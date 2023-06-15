from configparser import ConfigParser
from os.path import abspath, dirname, join
from typing import Any, List

from cachetools import TTLCache

from structlog import get_logger

log = get_logger(name=__name__)

CONFIG_ROOT = dirname(dirname(abspath(__file__)))

log.info(f"config_root={str(CONFIG_ROOT)}")


class SpaceTradersConfig(ConfigParser):
    """
    Basic configuration parser.
    Reads all .ini files and stores the values in config.
    """

    def __init__(self, config_path: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.config_path = config_path

        self.read(self.get_config_files())

    def get_config_files(self) -> List[str]:
        """
        Takes all .ini files in the root dir and
        generates config vars from them
        """

        files = [
            join(self.config_path, "env.ini"),
        ]

        return files


class SpaceTradersCache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        self.cache.clear()


config = SpaceTradersConfig(config_path=CONFIG_ROOT)
cache: TTLCache = TTLCache(maxsize=64, ttl=60)
