"""
数据库配置
"""
from typing import List

from fastapi import APIRouter
from sqlmodel import select

from app.dependencies import SessionDep
from app.exception import BusinessException, ErrorEnum
from app.models.first_model import Domain
from app.models.resp import Resp
from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/domain", tags=["域名环境"])


@router.get("/", description="查询所有", response_model=Resp[List[Domain]])
async def get_endpoints(session: SessionDep, skip: int = 0, limit: int = 100) -> Resp[List[Domain]]:
    statement = select(Domain).offset(skip).limit(limit)
    return Resp.success(session.exec(statement).all())


@router.get("/{item_id}", description="查询单个", response_model=Resp[Domain])
async def get_endpoint(item_id: int, session: SessionDep) -> Resp[Domain]:
    return Resp.success(session.get(Domain, item_id))


@router.delete("/{item_id}", description="删除单个", response_model=Resp[Domain])
async def delete_endpoint(item_id: int, session: SessionDep) -> Resp[Domain]:
    domain = session.get(Domain, item_id)
    if domain is None:
        raise BusinessException(ErrorEnum.NOT_FOUND)
    session.delete(domain)
    session.commit()
    return Resp.success(domain)


@router.post("/", description="新增单个", response_model=Resp[Domain])
async def create_endpoint(domain: Domain, session: SessionDep) -> Resp[Domain]:
    domain = Domain(name=domain.name, code=domain.code, environment=domain.environment, domain=domain.domain)
    session.add(domain)
    session.commit()
    return Resp.success(domain)


@router.put("/", description="修改单个", response_model=Resp[Domain])
async def update_endpoint(domain: Domain, session: SessionDep) -> Resp[Domain]:
    db_domain = session.get(Domain, domain.id)
    if db_domain is None:
        raise BusinessException(ErrorEnum.NOT_FOUND)
    domain = domain.model_dump(exclude_unset=True)
    db_domain.sqlmodel_update(domain)
    session.add(db_domain)
    session.commit()
    session.refresh(db_domain)
    return Resp.success(db_domain)
