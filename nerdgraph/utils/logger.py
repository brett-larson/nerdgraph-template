import logging
import os
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'time': self.formatTime(record, self.datefmt),
            'name': record.name,
            'level': record.levelname,
            'message': record.getMessage(),
        }
        return json.dumps(log_record)

def setup_logger(name: str) -> logging.Logger:
    """
    Setup a logger with a file handler and a console handler.
    :param name: Name of the logger
    :return: Logger object
    """

    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger

    # Create JSON formatter
    json_formatter = JsonFormatter()

    # File handler - using date in filename
    log_file = os.path.join(
        log_dir,
        f'app_{datetime.now().strftime("%Y%m%d")}.log'
    )
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(json_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(json_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger