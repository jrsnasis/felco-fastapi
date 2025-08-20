# app/core/logging.py
import logging
import sys
from typing import Any, Dict
from app.core.config import get_settings

settings = get_settings()


class RequestIDFilter(logging.Filter):
    """Filter to add request_id to log records"""
    
    def filter(self, record):
        # Add request_id if not already present
        if not hasattr(record, 'request_id'):
            record.request_id = getattr(record, 'request_id', 'no-request-id')
        return True


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def __init__(self, *args, use_colors=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_colors = use_colors
    
    def format(self, record):
        record_copy = logging.makeLogRecord(record.__dict__)
        
        # Add color to level name for console output
        if self.use_colors:
            levelname = record_copy.levelname
            if levelname in self.COLORS:
                record_copy.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        return super().format(record_copy)


def setup_logging():
    """Configure logging for the application"""
    
    # Base format string
    base_format = "%(asctime)s | %(levelname)-8s | %(request_id)s | %(name)s | %(message)s"
    detailed_format = "%(asctime)s | %(levelname)-8s | %(request_id)s | %(name)s | [%(filename)s:%(lineno)d] | %(message)s"
    
    # Use detailed format in development
    log_format = detailed_format if settings.is_development() else base_format
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.get_log_level())
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create request ID filter
    request_filter = RequestIDFilter()
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = ColoredFormatter(
        fmt=log_format,
        datefmt="%H:%M:%S",
        use_colors=True
    )
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(request_filter)
    console_handler.setLevel(settings.get_log_level())
    
    # Add console handler to root logger
    root_logger.addHandler(console_handler)
    
    # File handler only in development for debugging
    if settings.is_development():
        import os
        try:
            os.makedirs("logs", exist_ok=True)
            file_handler = logging.FileHandler(
                filename=f"logs/app.log",
                encoding='utf8'
            )
            file_formatter = logging.Formatter(
                fmt=log_format,
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(file_formatter)
            file_handler.addFilter(request_filter)
            file_handler.setLevel(logging.DEBUG)
            root_logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not create file handler: {e}")
    
    # Configure specific loggers with cleaner setup
    loggers_config = {
        "app": settings.get_log_level(),
        "uvicorn": "INFO",
        "uvicorn.error": "INFO",
        "uvicorn.access": "WARNING",
        "sqlalchemy.engine": "WARNING",
        "sqlalchemy.pool": "ERROR",
    }
    
    for logger_name, level in loggers_config.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.propagate = True
    
    # Set up app logger and log initial message
    app_logger = logging.getLogger("app")
    app_logger.info(f"Logging configured - Environment: {settings.ENVIRONMENT} | Level: {settings.get_log_level()}")
    
    return app_logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(f"app.{name}")