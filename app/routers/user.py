"""
数据库配置
"""

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.dependencies import HeaderDep, SessionDep, UserDep
from app.models.first_model import User
from app.models.resp import Resp
from app.schemes.user_scheme import UserLogin
from app.utils.encrypt_utils import verify_password
from app.utils.log_utils import Log
from app.utils.redis_utils import RedisClient
from app.utils.snow_utils import snowflake_generator

logger = Log().get_logger()

router = APIRouter(prefix="/user", tags=["用户"])


@router.post("/login", summary="登陆")
async def login(user: UserLogin, session: SessionDep) -> Resp[dict[str, str]]:
    statement = select(User).where(User.username == user.username)
    db_user = session.exec(statement).first()
    logger.info(f"查询用户的结果:{db_user}")
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或者密码错误")
    if not verify_password(str(user.password), str(db_user.password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或者密码错误")
    token = f"token_{snowflake_generator.generate_id()}"
    RedisClient().set(token, str(db_user.id), 30 * 60)
    return Resp.success({"token": token})


@router.post("/info", summary="查询权限")
async def get_info(user: UserDep) -> Resp[dict[str, str]]:
    return Resp.success({"roles": "admin", "name": user.username, "avatar": "", "introduction": ""})


@router.post("/logout", summary="退出")
async def delete_domain(token: HeaderDep, _user: UserDep) -> Resp[bool]:
    return Resp.success(bool(RedisClient().delete(token)))
