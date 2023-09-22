from pathlib import Path
import sys
from loguru import logger
from ..settings.settings import settings


def configure_logging(env):
    # Remove default logger
    logger.remove()

    # Set log format
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    # Log file path
    app_dir = ensure_app_dir()
    log_file_path = app_dir / settings.log_file_name

    # Configuration for development
    if env == 'dev':
        logger.add(log_file_path, level='DEBUG', format=log_format,
                   rotation="1 week", retention="10 days", compression="zip")
        logger.add(sys.stderr, level='DEBUG', format=log_format, colorize=True)

    # Configuration for production
    elif env == 'prod':
        # Log info and above to a file, and critical errors to stderr
        logger.add(log_file_path, level='INFO', format=log_format,
                   rotation="1 week", retention="10 days", compression="zip")
        logger.add(sys.stderr, level='CRITICAL',
                   format=log_format, colorize=True)

    else:
        raise ValueError(f"Unknown environment: {env}")


def ensure_app_dir() -> Path:
    app_dir = Path.home() / settings.app_directory
    if not app_dir.exists():
        app_dir.mkdir(parents=True)
    return app_dir
