"""
数据库配置
"""

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.dependencies import HeaderDep, SessionDep
from app.models.first_model import Domain, User
from app.models.resp import Resp
from app.schemes.user_scheme import UserLogin
from app.utils.encrypt_utils import verify_password
from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/user", tags=["用户"])


@router.post("/login", summary="登陆")
async def login(user: UserLogin, session: SessionDep) -> Resp[dict[str, str]]:
    statement = select(User).where(User.username == user.username)
    db_user = session.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="账号或密码错误")
    if not verify_password(str(user.password), str(db_user.password)):
        raise HTTPException(status_code=401, detail="账号或密码错误")
    token = {"token": "admin-token"}
    return Resp.success(token)


@router.post("/info", summary="查询权限")
async def get_info(token: HeaderDep) -> Resp[Domain]:
    return Resp.success(token)


@router.post("/logout", summary="退出")
async def delete_domain(token: HeaderDep) -> bool:
    return Resp.success(token)
