import logging
from contextvars import ContextVar
from logging.handlers import TimedRotatingFileHandler

from app.config import settings
from app.utils.wrapper_utils import singleton

# 声明上下文变量
trace_id: ContextVar[str] = ContextVar("trace_id", default="-")


class TraceIdFilter(logging.Filter):
    def filter(self, record):
        # 将当前上下文中的 trace_id 注入到日志记录中
        record.trace_id = trace_id.get() or '-'
        # if "-" == record.trace_id:
        #     token = str(uuid.uuid4()).replace("-", "")
        #     trace_id.set(token)
        #     record.trace_id = token
        return True


@singleton
class Log:

    def __init__(self):
        # 如果已经初始化了就不再执行，避免重复添加handle
        fmt_str = "%(asctime)s【%(levelname)s】-%(filename)s[%(lineno)d][%(trace_id)s]: %(message)s"
        self.fmt = logging.Formatter(fmt_str)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 添加handle
        self.logger.addHandler(self.console_handle())
        self.logger.addHandler(self.file_handle())
        self.modify_logger(["uvicorn.access", "uvicorn.error"])

    def modify_logger(self, names: list[str]):
        """
        将其他logger的输出重定向
        :param names: 名称
        """
        for name in names:
            logger = logging.getLogger(name)
            logger.handlers.clear()
            logger.addHandler(self.console_handle())
            logger.addHandler(self.file_handle())

    def file_handle(self) -> logging.Handler:
        """日志文件的handle"""
        file_handle = TimedRotatingFileHandler(settings.log_file, when='midnight', backupCount=5, encoding='utf-8')
        file_handle.setLevel(logging.INFO)
        file_handle.setFormatter(self.fmt)
        file_handle.addFilter(TraceIdFilter())
        return file_handle

    def console_handle(self) -> logging.Handler:
        """控制台日志的handle"""
        console_handle = logging.StreamHandler()
        console_handle.setLevel(logging.DEBUG)
        console_handle.setFormatter(self.fmt)
        console_handle.addFilter(TraceIdFilter())
        return console_handle

    def get_logger(self) -> logging.Logger:
        return self.logger
