# logging_config.py
import logging
from pprint import pformat

class CustomFormatter(logging.Formatter):
    def format(self, record):
        dt = self.formatTime(record, datefmt="[%d/%m/%y - %H:%M:%S]")
        return f"{dt} {record.levelname}: {record.getMessage()}"

def setup_logging(level=logging.INFO):
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(level)