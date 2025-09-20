"""
参数信息
"""

from typing import List, Optional

from fastapi import APIRouter

from app.core.dependencies import SessionDep
from app.core.exception import Resp
from app.dao import Dao
from app.models.first_model import CustomParameter
from app.vo import IdReq, PageReq
from app.vo.parameter_vo import InsertReq, SearchVo, UpdateReq

router = APIRouter(tags=["参数"])


@router.post("/parameter/add", summary="新增单个")
async def create(session: SessionDep, parm: InsertReq) -> Resp[CustomParameter]:
    parm = CustomParameter.model_validate(parm)
    result = Dao(session, CustomParameter).insert(parm)
    return Resp.success(result)


@router.post("/parameter/delete", summary="删除单个")
async def delete(session: SessionDep, parm: IdReq) -> Resp[bool]:
    flag = Dao(session, CustomParameter).delete_by_id(parm.id)
    return Resp.success(flag)


@router.post("/parameter/update", summary="修改单个")
async def update(session: SessionDep, parm: UpdateReq) -> Resp[bool]:
    flag = Dao(session, CustomParameter).update_by_id(parm)
    return Resp.success(flag)


@router.post("/parameter/query", summary="查询所有")
async def query(session: SessionDep, parm: PageReq[SearchVo]) -> Resp[List[CustomParameter]]:
    results = Dao(session, CustomParameter).query(parm)
    return Resp.success(results)


@router.post("/parameter/statistic", summary="统计")
async def statistic(session: SessionDep, parm: PageReq[SearchVo]) -> Resp[List[int]]:
    results = Dao(session, CustomParameter).statistic(parm)
    return Resp.success(results)


@router.post("/parameter/info", summary="查询单个")
async def info(session: SessionDep, parm: IdReq) -> Resp[Optional[CustomParameter]]:
    results = Dao(session, CustomParameter).query_by_id(parm.id)
    return Resp.success(results)
