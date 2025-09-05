"""
定时任务
"""
from fastapi import APIRouter

router = APIRouter(prefix="/schedule", tags=["定时任务"])  # 接口文档中的标签
