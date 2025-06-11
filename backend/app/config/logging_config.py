# logging_config.py
import logging
from pprint import pformat

class CustomFormatter(logging.Formatter):
    GREEN = "\033[92m"   # Vert pour INFO
    YELLOW = "\033[93m"  # Jaune pour le nom de fichier
    BLUE = "\033[94m"    # Bleu clair pour l'heure
    RESET = "\033[0m"

    def format(self, record):
        dt = self.formatTime(record, datefmt="%d/%m/%y - %H:%M:%S")
        dt_colored = f"[{self.BLUE}{dt}{self.RESET}]"
        levelname = record.levelname
        if record.levelno == logging.INFO:
            levelname = f"[{self.GREEN}{levelname}{self.RESET}]"
        filename_colored = f"[{self.YELLOW}{record.filename}{self.RESET}]"
        base_msg = f"{dt_colored} {levelname} {filename_colored}: {record.getMessage()}"
        return base_msg

def setup_logging(level=logging.INFO):
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(level)