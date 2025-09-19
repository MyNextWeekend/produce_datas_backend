"""
数据库配置
"""

from fastapi import APIRouter

from app.core.dependencies import SessionDep, UserDep
from app.core.exception import BusinessException, ErrorEnum, Resp
from app.dao.user import UserDao
from app.services.user_service import UserService
from app.utils.encrypt_utils import verify_password
from app.utils.log_utils import logger
from app.vo.user_vo import UserLogin

router = APIRouter(tags=["用户"])


@router.post("/user/login", summary="登陆")
async def login(user: UserLogin, session: SessionDep) -> Resp[dict[str, str]]:
    db_user = UserDao(session).query_by_username(user.username)
    logger.info(f"查询用户的结果:{db_user}")
    if not db_user:
        raise BusinessException.new(ErrorEnum.INVALID_CREDENTIALS)
    if not verify_password(str(user.password), str(db_user.password)):
        raise BusinessException.new(ErrorEnum.INVALID_CREDENTIALS)
    user = UserService.from_user(db_user)
    return Resp.success({"token": user.token})


@router.post("/user/info", summary="查询权限")
async def get_info(user: UserDep) -> Resp[dict[str, str]]:
    return Resp.success({"roles": "admin", "name": user.username, "avatar": "", "introduction": ""})


@router.post("/user/logout", summary="退出")
async def logout(user: UserDep) -> Resp[bool]:
    return Resp.success(bool(user.logout()))
