# Handles the logging configuration for the application

import logging
import logging.config
from enum import Enum
from logging.config import dictConfig

from src.config import config


class LoggerName(Enum):
    APP = "app"
    ALGORITHM = "app.algorithm"


def init_loggers() -> None:
    """Initialize the loggers for the application"""

    logger_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "app": {"handlers": ["default"], "level": "DEBUG"},
            "app.algorithm": {"handlers": ["default"], "level": "ERROR"},
            "psycopg": {"handlers": ["default"], "level": "INFO"},
            "psycopg.pool": {"handlers": ["default"], "level": "INFO"},
        },
    }

    dictConfig(logger_config)

    logging.getLogger("app").setLevel(config.logger_level)


def get_logger(name: LoggerName = LoggerName.APP) -> logging.Logger:
    """Get the logger for the application"""
    return logging.getLogger(name.value)
