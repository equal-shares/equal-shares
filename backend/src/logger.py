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
    # Store initialized state in a module-level variable
    if hasattr(init_loggers, '_initialized'):
        return
        
    # Remove any existing handlers from the root logger
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
            
    logger_config = {
        "version": 1,
        "disable_existing_loggers": True,  # Prevent existing loggers from interfering
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
            "app": {
                "handlers": ["default"],
                "level": "DEBUG",
                "propagate": False,  # Prevent propagation to avoid duplication
            },
            "app.algorithm": {
                "handlers": ["default"],
                "level": "DEBUG",
                "propagate": False,  # Prevent propagation to avoid duplication
            },
            "psycopg": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "psycopg.pool": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }

    # Apply the configuration
    dictConfig(logger_config)

    # Set specific log levels from config
    logging.getLogger("app").setLevel(config.logger_level)
    logging.getLogger("app.algorithm").setLevel(config.logger_level)
    
    # Mark as initialized
    init_loggers._initialized = True

def get_logger(name: LoggerName = LoggerName.APP) -> logging.Logger:
    """Get the logger for the application"""
    # Ensure loggers are initialized
    init_loggers()
    return logging.getLogger(name.value)
