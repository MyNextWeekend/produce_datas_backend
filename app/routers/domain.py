"""
数据库配置
"""

from typing import List

from fastapi import APIRouter
from sqlmodel import select

from app.core.dependencies import SessionDep
from app.core.exception import BusinessException, ErrorEnum, Resp
from app.models.first_model import Domain
from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/domain", tags=["域名环境"])


@router.get("/", summary="查询所有")
async def get_domains(session: SessionDep, skip: int = 0, limit: int = 100) -> Resp[List[Domain]]:
    statement = select(Domain).offset(skip).limit(limit)
    return Resp.success(session.exec(statement).all())


@router.get("/{item_id}", summary="查询单个")
async def get_domain(item_id: int, session: SessionDep) -> Resp[Domain]:
    return Resp.success(session.get(Domain, item_id))


@router.delete("/{item_id}", summary="删除单个")
async def delete_domain(item_id: int, session: SessionDep) -> Resp[Domain]:
    domain = session.get(Domain, item_id)
    if domain is None:
        raise BusinessException.new(ErrorEnum.NOT_FOUND)
    session.delete(domain)
    session.commit()
    return Resp.success(domain)


@router.post("/", summary="新增单个")
async def create_domain(domain: Domain, session: SessionDep) -> Resp[Domain]:
    domain = Domain(name=domain.name, code=domain.code, environment=domain.environment, domain=domain.domain)
    session.add(domain)
    session.commit()
    return Resp.success(domain)


@router.put("/", summary="修改单个")
async def update_domain(domain: Domain, session: SessionDep) -> Resp[Domain]:
    db_domain = session.get(Domain, domain.id)
    if db_domain is None:
        raise BusinessException.new(ErrorEnum.NOT_FOUND)
    domain_dic = domain.model_dump(exclude_unset=True)
    db_domain.sqlmodel_update(domain_dic)
    session.add(db_domain)
    session.commit()
    session.refresh(db_domain)
    return Resp.success(db_domain)
