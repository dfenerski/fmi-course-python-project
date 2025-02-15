import logging
import sys


class Logger:
    def __init__(self, logger_name=""):
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.logger = logging.getLogger(logger_name)  # hey whatsup with the casing

    def log(self, value):
        self.logger.info(value)

    def warn(self, value):
        self.logger.warning(value)

    def error(self, value):
        self.logger.error(value)
