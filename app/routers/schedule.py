"""
定时任务
"""
from fastapi import APIRouter

from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/schedule", tags=["定时任务"])  # 接口文档中的标签
