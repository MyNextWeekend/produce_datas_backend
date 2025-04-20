"""
报告相关
"""

from typing import List

from fastapi import APIRouter
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.first_model import Report
from app.models.resp import Resp
from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/report", tags=["报告"])


@router.get("/", description="查询所有", response_model=Resp[List[Report]])
async def get_reports(session: SessionDep, skip: int = 0, limit: int = 100) -> Resp[List[Report]]:
    statement = select(Report).offset(skip).limit(limit)
    return Resp.success(session.exec(statement).all())


@router.get("/{item_id}", description="查询单个", response_model=Resp[Report])
async def get_report(item_id: int, session: SessionDep) -> Resp[Report]:
    return Resp.success(session.get(Report, item_id))
