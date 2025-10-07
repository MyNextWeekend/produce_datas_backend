"""
数据库配置
"""

from typing import List, Optional

from fastapi import APIRouter

from app.core.dependencies import SessionDep, UserDep
from app.core.exception import BusinessException, ErrorEnum, Resp
from app.dao import Dao
from app.dao.user import UserDao
from app.models.first_model import User
from app.services.user_service import UserService
from app.utils.encrypt_utils import get_password_hash, verify_password
from app.utils.log_utils import logger
from app.vo import IdReq, PageReq, StatisticResp
from app.vo.user_vo import InsertReq, SearchVo, UpdateReq, UserLogin

router = APIRouter(tags=["用户"])


@router.post("/user/login", summary="登陆")
async def login(session: SessionDep, user: UserLogin) -> Resp[dict[str, str]]:
    db_user = UserDao(session).query_by_username(user.username)
    logger.info(f"查询用户的结果:{db_user}")
    if not db_user:
        raise BusinessException.new(ErrorEnum.INVALID_CREDENTIALS)
    if not verify_password(str(user.password), str(db_user.password)):
        raise BusinessException.new(ErrorEnum.INVALID_CREDENTIALS)
    user = UserService.from_user(db_user)
    return Resp.success({"token": user.token})


@router.post("/user/permission", summary="权限信息")
async def permission(user: UserDep) -> Resp[dict[str, str]]:
    return Resp.success({"roles": ["admin"], "name": user.db_user.username, "avatar": "", "introduction": ""})


@router.post("/user/logout", summary="退出")
async def logout(user: UserDep) -> Resp[bool]:
    return Resp.success(bool(user.logout()))


@router.post("/user/add", summary="新增单个")
async def create(session: SessionDep, parm: InsertReq) -> Resp[User]:
    obj = User.model_validate(parm)
    obj.is_active = 1
    obj.password = get_password_hash(obj.password)
    domain = Dao(session, User).insert(obj)
    return Resp.success(domain)


@router.post("/user/delete/", summary="删除单个")
async def delete(session: SessionDep, parm: IdReq) -> Resp[bool]:
    flag = Dao(session, User).delete_by_id(parm.id)
    return Resp.success(flag)


@router.post("/user/update", summary="修改单个")
async def update(session: SessionDep, parm: UpdateReq) -> Resp[bool]:
    flag = Dao(session, User).update_by_id(parm)
    if not flag:
        raise BusinessException.new(ErrorEnum.NOT_FOUND)
    return Resp.success(flag)


@router.post("/user/query", summary="查询所有")
async def query(session: SessionDep, parm: PageReq[SearchVo]) -> Resp[List[User]]:
    result = Dao(session, User).query(parm)
    return Resp.success(result)


@router.post("/user/statistic", summary="统计")
async def statistic(session: SessionDep, parm: PageReq[SearchVo]) -> Resp[StatisticResp]:
    total = Dao(session, User).statistic(parm)
    return Resp.success(StatisticResp(total=total))


@router.post("/user/info", summary="查询单个")
async def info(session: SessionDep, parm: IdReq) -> Resp[Optional[User]]:
    result = Dao(session, User).query_by_id(parm.id)
    return Resp.success(result)
