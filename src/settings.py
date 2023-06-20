from configparser import ConfigParser
from os import environ
from os.path import abspath, dirname, join
from typing import Any, List

from structlog import get_logger

log = get_logger(name=__name__)

CONFIG_ROOT = dirname(dirname(abspath(__file__)))
ENVIRONMENT = environ.get("ENVIRONMENT", "development")
IN_DEVELOPMENT = ENVIRONMENT == "development"


def database_url():
    host = config.get("database", "host")
    port = config.get("database", "port")
    name = config.get("database", "name")
    username = config.get("database", "username")
    password = config.get("database", "password")

    parts = ["postgresql://"]

    if username:
        parts.append(username)

    if password and username != "readonly":
        parts.append(":")
        parts.append(password)

    if username or password:
        parts.append("@")

    if host:
        parts.append(host)

    if port:
        parts.append(":")
        parts.append(port)

    parts.append("/")
    if name is not None:
        parts.append(name)
    # handles the password as a token - used in development (local) only
    if IN_DEVELOPMENT and password and username == "readonly":
        parts.append("&sslmode=require")
        parts.append("&password=" + password)
    return "".join(parts)


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
