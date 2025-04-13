"""
接口配置信息
"""
from typing import List

from fastapi import APIRouter
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.first_model import Endpoint
from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/endpoint", tags=["接口配置"])


@router.get("/", description="查询所有", response_model=List[Endpoint])
async def get_endpoints(session: SessionDep, skip: int = 0, limit: int = 100) -> List[Endpoint]:
    statement = select(Endpoint).offset(skip).limit(limit)
    return session.exec(statement).all()


@router.get("/{item_id}", description="查询单个", response_model=Endpoint)
async def get_endpoint(item_id: int, session: SessionDep) -> Endpoint:
    return session.get(Endpoint, item_id)


@router.delete("/{item_id}", description="删除单个", response_model=Endpoint)
async def delete_endpoint(item_id: int, session: SessionDep) -> Endpoint:
    endpoint = session.get(Endpoint, item_id)
    if endpoint is None:
        raise HTTPException(status_code=404)
    session.delete(endpoint)
    session.commit()
    return endpoint


@router.post("/", description="新增单个", response_model=Endpoint)
async def create_endpoint(endpoint: Endpoint, session: SessionDep) -> Endpoint:
    endpoint = Endpoint(name=endpoint.name, code=endpoint.code, method=endpoint.method, path=endpoint.path,
                        description=endpoint.description)
    session.add(endpoint)
    session.commit()
    return endpoint


@router.put("/", description="修改单个", response_model=Endpoint)
async def update_endpoint(endpoint_new: Endpoint, session: SessionDep) -> Endpoint:
    db_endpoint = session.get(Endpoint, endpoint_new.id)
    endpoint_new = endpoint_new.model_dump(exclude_unset=True)
    db_endpoint.sqlmodel_update(endpoint_new)
    session.add(db_endpoint)
    session.commit()
    session.refresh(db_endpoint)
    return db_endpoint
