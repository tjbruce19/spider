import logging
import sys

class UrlLogger():
    def __init__(self,name="",level=None):
        self.logger = self.__get_logger(name)
        if level is None:
            self.level = logging.INFO

    def __get_logger(self, name=""):
        _logger = logging.getLogger(name)
        _logger.setLevel(level=logging.DEBUG)
        return _logger

    def file_handler(self, file_name):
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(level=self.level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.hasHandlers()
        self.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(level=logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
