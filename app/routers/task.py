"""
任务相关
"""
from fastapi import APIRouter

from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/task", tags=["任务操作"])
