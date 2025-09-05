"""
参数信息
"""

from typing import List

from fastapi import APIRouter
from sqlmodel import select

from app.core.dependencies import SessionDep
from app.core.exception import BusinessException, ErrorEnum, Resp
from app.models.first_model import CustomParameter

router = APIRouter(prefix="/parameter", tags=["参数"])


@router.get("/", summary="查询所有")
async def get_parameters(session: SessionDep, skip: int = 0, limit: int = 100) -> Resp[List[CustomParameter]]:
    statement = select(CustomParameter).offset(skip).limit(limit)
    return Resp.success(session.exec(statement).all())


@router.get("/{item_id}", summary="查询单个")
async def get_parameter(item_id: int, session: SessionDep) -> Resp[CustomParameter]:
    return Resp.success(session.get(CustomParameter, item_id))


@router.delete("/{item_id}", summary="删除单个")
async def delete_parameter(item_id: int, session: SessionDep) -> Resp[CustomParameter]:
    custom_parameter = session.get(CustomParameter, item_id)
    if CustomParameter is None:
        raise BusinessException.new(ErrorEnum.NOT_FOUND)
    session.delete(custom_parameter)
    session.commit()
    return Resp.success(custom_parameter)


@router.post("/", summary="新增单个")
async def create_parameter(custom_parameter: CustomParameter, session: SessionDep) -> Resp[CustomParameter]:
    custom_parameter = CustomParameter(key_name=custom_parameter.key_name, value=custom_parameter.value)
    session.add(custom_parameter)
    session.commit()
    return Resp.success(custom_parameter)


@router.put("/", summary="修改单个")
async def update_parameter(custom_parameter: CustomParameter, session: SessionDep) -> Resp[CustomParameter]:
    db_custom_parameter = session.get(CustomParameter, custom_parameter.id)
    if db_custom_parameter is None:
        raise BusinessException.new(ErrorEnum.NOT_FOUND)
    custom_parameter_dic = custom_parameter.model_dump(exclude_unset=True)
    db_custom_parameter.sqlmodel_update(custom_parameter_dic)
    session.add(db_custom_parameter)
    session.commit()
    session.refresh(db_custom_parameter)
    return Resp.success(db_custom_parameter)
