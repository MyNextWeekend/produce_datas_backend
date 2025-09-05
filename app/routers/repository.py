"""
远端仓库
"""
from typing import List

from fastapi import APIRouter
from sqlmodel import select

from app.core.dependencies import SessionDep
from app.core.exception import BusinessException, ErrorEnum, Resp
from app.models.first_model import Repository

router = APIRouter(prefix="/repository", tags=["仓库操作"])  # 接口文档中的标签


@router.get("/", summary="查询所有")
async def get_repositories(session: SessionDep, skip: int = 0, limit: int = 100) -> Resp[List[Repository]]:
    statement = select(Repository).offset(skip).limit(limit)
    return Resp.success(session.exec(statement).all())


@router.get("/{item_id}", summary="查询单个")
async def get_repository(item_id: int, session: SessionDep) -> Resp[Repository]:
    return Resp.success(session.get(Repository, item_id))


# @router.get("/{item_id}/clone", summary="克隆仓库")
# async def clone_repository(item_id: int, session: SessionDep) -> Resp[Repository]:
#     repository = session.get(Repository, item_id)
#     if not repository:
#         raise BusinessException(ErrorEnum.NOT_FOUND)
#     # TODO clone仓库到本地，然后数据库新增一条数据
#     return Resp.success(data=)


@router.delete("/{item_id}", summary="删除单个")
async def delete_repository(item_id: int, session: SessionDep) -> Resp[Repository]:
    repository = session.get(Repository, item_id)
    if Repository is None:
        raise BusinessException.new(ErrorEnum.NOT_FOUND)
    session.delete(repository)
    session.commit()
    return Resp.success(repository)


@router.post("/", summary="新增单个")
async def create_repository(repository: Repository, session: SessionDep) -> Resp[Repository]:
    repository = Repository(name=repository.name, url=repository.url)
    session.add(repository)
    session.commit()
    return Resp.success(repository)


@router.put("/", summary="修改单个")
async def update_repository(repository: Repository, session: SessionDep) -> Resp[Repository]:
    db_repository = session.get(Repository, repository.id)
    if db_repository is None:
        raise BusinessException.new(ErrorEnum.NOT_FOUND)
    repository_json = repository.model_dump(exclude_unset=True)
    db_repository.sqlmodel_update(repository_json)
    session.add(db_repository)
    session.commit()
    session.refresh(db_repository)
    return Resp.success(db_repository)
