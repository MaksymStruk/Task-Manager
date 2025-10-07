from loguru import logger
import sys

handlers = [
    {
        "sink": "logs/.logfile.log",
        "level": "TRACE",
        "format": "[{time:YYYY-MM-DD HH:mm:ss} UTC] - [{level:7}] - [{name:10}:{line}] - {message}",
        "colorize": False,
        "rotation": "31 day",
        "compression": "zip",
        "enqueue": True,
        "catch": True,
    },
    {
        "sink": "logs/.errorfile.log",
        "level": "WARNING",
        "format": "[{time:YYYY-MM-DD HH:mm:ss} UTC] - [{level:7}] - [{name:10}:{line}] - {message}",
        "colorize": False,
        "rotation": "31 day",
        "compression": "zip",
        "enqueue": True,
        "catch": True,
    },
    {
        "sink": sys.stdout,
        "level": "TRACE",
        "format": "<level>[{time:YYYY-MM-DD HH:mm:ss} UTC] - [{level:7}] - [{name:10}:{line}] - {message}</level>",
        "colorize": True,
        "enqueue": True,
        "catch": True,
    }
]

logger.configure(handlers=handlers)

def logger_test():
    logger.trace("Тестове TRACE повідомлення")
    logger.debug("Тестове DEBUG повідомлення")
    logger.info("Тестове INFO повідомлення")
    logger.success("Тестове SUCCESS повідомлення")
    logger.warning("Тестове WARNING повідомлення")
    logger.error("Тестове ERROR повідомлення")
    logger.critical("Тестове CRITICAL повідомлення")

custom_logger = logger