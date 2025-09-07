"""
数据库配置
"""

from typing import List

from fastapi import APIRouter

from app.core.dependencies import SessionDep
from app.core.exception import BusinessException, ErrorEnum, Resp
from app.dao import Dao
from app.models.first_model import Domain
from app.vo import IdReq, PageReq
from app.vo.domain_vo import InsertVO, SearchVO, UpdateVO

router = APIRouter(tags=["域名环境"])


@router.post("/domain/info", summary="查询单个")
async def get_domain(session: SessionDep, parm: IdReq) -> Resp[Domain]:
    result = Dao(session, Domain).query_by_id(parm.id)
    return Resp.success(result)


@router.post("/domain/query", summary="查询所有")
async def query_domain(session: SessionDep, parm: PageReq[SearchVO]) -> Resp[List[Domain]]:
    result = Dao(session, Domain).query(parm)
    return Resp.success(result)


@router.post("/domain/delete/", summary="删除单个")
async def delete_domain(session: SessionDep, parm: IdReq) -> Resp[bool]:
    flag = Dao(session, Domain).delete_by_id(parm.id)
    return Resp.success(flag)


@router.post("/domain/add", summary="新增单个")
async def create_domain(session: SessionDep, parm: InsertVO) -> Resp[Domain]:
    obj = Domain.model_validate(parm)
    domain = Dao(session, Domain).insert(obj)
    return Resp.success(domain)


@router.post("/domain/update", summary="修改单个")
async def update_domain(session: SessionDep, parm: UpdateVO) -> Resp[bool]:
    flag = Dao(session, Domain).update_by_id(parm)
    if not flag:
        raise BusinessException.new(ErrorEnum.NOT_FOUND)
    return Resp.success(flag)
