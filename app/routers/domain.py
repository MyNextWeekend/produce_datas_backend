"""
数据库配置
"""
from fastapi import APIRouter

from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/domain", tags=["域名环境"])
