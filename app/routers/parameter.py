"""
参数信息
"""

from typing import List

from fastapi import APIRouter
from sqlmodel import select

from app.dependencies import SessionDep
from app.exception import BusinessException, ErrorEnum
from app.models.first_model import CustomParameter
from app.models.resp import Resp
from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/parameter", tags=["参数"])


@router.get("/", description="查询所有", response_model=Resp[List[CustomParameter]])
async def get_parameters(session: SessionDep, skip: int = 0, limit: int = 100) -> Resp[List[CustomParameter]]:
    statement = select(CustomParameter).offset(skip).limit(limit)
    return Resp.success(session.exec(statement).all())


@router.get("/{item_id}", description="查询单个", response_model=Resp[CustomParameter])
async def get_parameter(item_id: int, session: SessionDep) -> Resp[CustomParameter]:
    return Resp.success(session.get(CustomParameter, item_id))


@router.delete("/{item_id}", description="删除单个", response_model=Resp[CustomParameter])
async def delete_parameter(item_id: int, session: SessionDep) -> Resp[CustomParameter]:
    custom_parameter = session.get(CustomParameter, item_id)
    if CustomParameter is None:
        raise BusinessException(ErrorEnum.NOT_FOUND)
    session.delete(custom_parameter)
    session.commit()
    return Resp.success(custom_parameter)


@router.post("/", description="新增单个", response_model=Resp[CustomParameter])
async def create_parameter(custom_parameter: CustomParameter, session: SessionDep) -> Resp[CustomParameter]:
    custom_parameter = CustomParameter(key_name=custom_parameter.key_name, value=custom_parameter.value)
    session.add(custom_parameter)
    session.commit()
    return Resp.success(custom_parameter)


@router.put("/", description="修改单个", response_model=Resp[CustomParameter])
async def update_parameter(custom_parameter: CustomParameter, session: SessionDep) -> Resp[CustomParameter]:
    db_custom_parameter = session.get(CustomParameter, custom_parameter.id)
    if db_custom_parameter is None:
        raise BusinessException(ErrorEnum.NOT_FOUND)
    custom_parameter_dic = custom_parameter.model_dump(exclude_unset=True)
    db_custom_parameter.sqlmodel_update(custom_parameter_dic)
    session.add(db_custom_parameter)
    session.commit()
    session.refresh(db_custom_parameter)
    return Resp.success(db_custom_parameter)
