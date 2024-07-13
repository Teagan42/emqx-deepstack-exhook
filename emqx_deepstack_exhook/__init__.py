import logging
from os import environ

logging.basicConfig(
    level=logging.getLevelNamesMapping()[environ.get("LOG_LEVEL", "INFO")]
)
