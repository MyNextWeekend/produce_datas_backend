import logging
from logging.handlers import TimedRotatingFileHandler

from ..config import settings
from .wrapper_utils import singleton


@singleton
class Log:

    def __init__(self):
        # 如果已经初始化了就不再执行，避免重复添加handle
        self.fmt_str = "%(asctime)s【%(levelname)s】-%(filename)s[%(lineno)d]: %(message)s"
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 添加handle
        self.logger.addHandler(self.console_handle())
        self.logger.addHandler(self.file_handle())
        self.modify_logger(["uvicorn", "uvicorn.access"])

    def modify_logger(self, names: list[str]):
        """
        将其他logger的输出重定向
        :param names: 名称
        """
        logger_list = []
        for name in names:
            logger_list.append(logging.getLogger(name))
        for logger in logger_list:
            logger.handlers.clear()
            logger.addHandler(self.console_handle())
            logger.addHandler(self.file_handle())

    def file_handle(self) -> logging.Handler:
        """日志文件的handle"""
        file_handle = TimedRotatingFileHandler(settings.log_file, when='midnight', backupCount=5, encoding='utf-8')
        file_handle.setLevel(logging.INFO)
        fmt = logging.Formatter(self.fmt_str)
        file_handle.setFormatter(fmt)
        return file_handle

    def console_handle(self) -> logging.Handler:
        """控制台日志的handle"""
        console_handle = logging.StreamHandler()
        console_handle.setLevel(logging.DEBUG)
        fmt = logging.Formatter(self.fmt_str)
        console_handle.setFormatter(fmt)
        return console_handle

    def get_logger(self) -> logging.Logger:
        return self.logger
