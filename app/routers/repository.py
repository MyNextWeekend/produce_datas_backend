"""
远端仓库
"""
from fastapi import APIRouter

from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/repository", tags=["仓库操作"])  # 接口文档中的标签
