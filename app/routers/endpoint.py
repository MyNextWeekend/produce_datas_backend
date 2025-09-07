"""
接口配置信息
"""

from typing import List, Optional

from fastapi import APIRouter

from app.core.dependencies import SessionDep
from app.core.exception import Resp
from app.dao import Dao
from app.models.first_model import Endpoint
from app.vo import IdReq, PageReq
from app.vo.endpoint_vo import InsertReq, SearchVo, UpdateReq

router = APIRouter(tags=["接口配置"])


@router.post("/endpoint/add", summary="新增单个")
async def create_endpoint(session: SessionDep, parm: InsertReq) -> Resp[bool]:
    parm = Endpoint.model_validate(parm)
    flag = Dao(session, Endpoint).insert(parm)
    return Resp.success(flag)


@router.delete("/endpoint/delete", summary="删除单个")
async def delete_endpoint(session: SessionDep, parm: IdReq) -> Resp[bool]:
    flag = Dao(session, Endpoint).delete_by_id(parm.id)
    return Resp.success(flag)


@router.put("/endpoint/update", summary="修改单个")
async def update_endpoint(session: SessionDep, parm: UpdateReq) -> Resp[bool]:
    flag = Dao(session, Endpoint).update_by_id(parm)
    return Resp.success(flag)


@router.post("/endpoint/query", summary="查询所有")
async def get_endpoints(session: SessionDep, parm: PageReq[SearchVo]) -> Resp[List[Endpoint]]:
    results = Dao(session, Endpoint).query(parm)
    return Resp.success(results)


@router.get("/endpoint/info", summary="查询单个")
async def get_endpoint(session: SessionDep, parm: IdReq) -> Resp[Optional[Endpoint]]:
    results = Dao(session, Endpoint).query_by_id(parm.id)
    return Resp.success(results)
