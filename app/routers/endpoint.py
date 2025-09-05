"""
接口配置信息
"""

from typing import List

from fastapi import APIRouter

from app.core.dependencies import SessionDep
from app.core.exception import BusinessException, ErrorEnum, Resp
from app.dao.endpoint import EndpointDao
from app.models.first_model import Endpoint
from app.vo import Query
from app.vo.endpoint_vo import SearchVo

router = APIRouter(tags=["接口配置"])


@router.post("/endpoint/query", summary="查询所有")
async def get_endpoints(session: SessionDep, query: Query[SearchVo]) -> Resp[List[Endpoint]]:
    result = EndpointDao.query(session, query)
    return Resp.success(result)


@router.get("/{item_id}", summary="查询单个")
async def get_endpoint(item_id: int, session: SessionDep) -> Resp[Endpoint]:
    return Resp.success(session.get(Endpoint, item_id))


@router.delete("/{item_id}", summary="删除单个")
async def delete_endpoint(item_id: int, session: SessionDep) -> Resp[Endpoint]:
    endpoint = session.get(Endpoint, item_id)
    if endpoint is None:
        raise BusinessException.new(ErrorEnum.NOT_FOUND)
    session.delete(endpoint)
    session.commit()
    return Resp.success(endpoint)


@router.post("/", summary="新增单个")
async def create_endpoint(endpoint: Endpoint, session: SessionDep) -> Resp[Endpoint]:
    endpoint = Endpoint(
        name=endpoint.name,
        code=endpoint.code,
        method=endpoint.method,
        path=endpoint.path,
        description=endpoint.description,
        domain_code=endpoint.domain_code,
    )
    session.add(endpoint)
    session.commit()
    return Resp.success(endpoint)


@router.put("/", summary="修改单个")
async def update_endpoint(endpoint_new: Endpoint, session: SessionDep) -> Resp[Endpoint]:
    db_endpoint = session.get(Endpoint, endpoint_new.id)
    if db_endpoint is None:
        raise BusinessException.new(ErrorEnum.NOT_FOUND)
    endpoint_dic = endpoint_new.model_dump(exclude_unset=True)
    db_endpoint.sqlmodel_update(endpoint_dic)
    session.add(db_endpoint)
    session.commit()
    session.refresh(db_endpoint)
    return Resp.success(db_endpoint)
