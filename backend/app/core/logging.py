from loguru import logger
import sys

_logger_configured = False


def configure_logging() -> None:
    global _logger_configured
    if _logger_configured:
        return
    logger.remove()
    logger.add(sys.stdout, level="INFO", enqueue=True, backtrace=False, diagnose=False,
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}")
    _logger_configured = True


def get_logger(name: str):
    configure_logging()
    return logger.bind(module=name)
