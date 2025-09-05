"""
报告相关
"""

from typing import List

from fastapi import APIRouter
from sqlmodel import select

from app.core.dependencies import SessionDep
from app.core.exception import Resp
from app.models.first_model import Report
from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/report", tags=["报告"])


@router.get("/", summary="查询所有")
async def get_reports(session: SessionDep, skip: int = 0, limit: int = 100) -> Resp[List[Report]]:
    statement = select(Report).offset(skip).limit(limit)
    return Resp.success(session.exec(statement).all())


@router.get("/{item_id}", summary="查询单个")
async def get_report(item_id: int, session: SessionDep) -> Resp[Report]:
    return Resp.success(session.get(Report, item_id))
