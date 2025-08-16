"""
接口配置信息
"""

from typing import List

from fastapi import APIRouter
from sqlmodel import select

from app.dependencies import SessionDep
from app.exception import BusinessException, ErrorEnum
from app.models.first_model import Endpoint
from app.models.resp import Resp
from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/endpoint", tags=["接口配置"])


@router.get("/", summary="查询所有")
async def get_endpoints(session: SessionDep, skip: int = 0, limit: int = 100) -> Resp[List[Endpoint]]:
    statement = select(Endpoint).offset(skip).limit(limit)
    return Resp.success(session.exec(statement).all())


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
