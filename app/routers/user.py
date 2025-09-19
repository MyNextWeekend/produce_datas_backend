"""
数据库配置
"""

from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import SessionDep, UserDep
from app.core.exception import Resp
from app.dao.user import UserDao
from app.services.user_service import UserService
from app.utils.encrypt_utils import verify_password
from app.utils.log_utils import logger
from app.vo.user_vo import UserLogin

router = APIRouter(prefix="/user", tags=["用户"])


@router.post("/login", summary="登陆")
async def login(user: UserLogin, session: SessionDep) -> Resp[dict[str, str]]:
    db_user = UserDao(session).query_by_username(user.username)
    logger.info(f"查询用户的结果:{db_user}")
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或者密码错误")
    if not verify_password(str(user.password), str(db_user.password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或者密码错误")
    user = UserService.from_user(db_user)
    return Resp.success({"token": user.token})


@router.post("/info", summary="查询权限")
async def get_info(user: UserDep) -> Resp[dict[str, str]]:
    return Resp.success({"roles": "admin", "name": user.username, "avatar": "", "introduction": ""})


@router.post("/logout", summary="退出")
async def delete_domain(user: UserDep) -> Resp[bool]:
    return Resp.success(bool(user.logout()))
