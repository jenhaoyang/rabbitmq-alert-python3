import logging
from logging import handlers
from sys import stdout

LOGGING_PATH = "rabbitmq-alert.log"

class Logger:

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        # File handler with rotation
        rotate_handler = handlers.TimedRotatingFileHandler(
            filename=LOGGING_PATH,
            when="midnight"
        )
        rotate_handler.suffix = "%Y%m%d"
        rotate_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        self.logger.addHandler(rotate_handler)

        # Standard output handler
        stdout_handler = logging.StreamHandler(stdout)
        stdout_handler.setFormatter(logging.Formatter("%(asctime)s: %(levelname)s - %(message)s"))
        self.logger.addHandler(stdout_handler)

    def get_logger(self):
        return self.logger

