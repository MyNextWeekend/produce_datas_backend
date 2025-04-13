"""
参数信息
"""
from fastapi import APIRouter

from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/parameter", tags=["参数"])
