import logging
from os import environ

logging.basicConfig(level=logging._nameToLevel[environ.get("LOG_LEVEL", "INFO")])

