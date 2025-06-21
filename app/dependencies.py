from collections.abc import Generator
from enum import Enum
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import create_engine
from sqlmodel import Session, select

from app.config import settings
from app.models.first_model import User
from app.utils.redis_utils import RedisClient

engine = create_engine(str(settings.sqlmodel_database_uri), echo=True, pool_size=8, pool_recycle=60 * 30)


def get_session() -> Generator[Session, None, None]:
    """
    为每个请求yield提供一个新的Session
    :return: 会话
    """
    with Session(engine) as session:
        yield session


# 为了简化代码
SessionDep = Annotated[Session, Depends(get_session)]
HeaderDep = Annotated[str | None, Header()]


def get_user_by_token(token: HeaderDep, session: SessionDep) -> User:
    """
    校验 请求头 header 中的 token
    并且从数据库获取 用户信息
    """
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或者密码错误")

    client = RedisClient()
    value = client.get(token)
    if value is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或者密码错误")

    statement = select(User).where(User.id == value)
    db_user = session.exec(statement).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或者密码错误")
    # 续 token 有效时间
    client.set(token, value, 30 * 60)
    return db_user


UserDep = Annotated[User, Depends(get_user_by_token)]


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


def require_role(required_role: Role):
    """
    管理 api 特定权限的用户访问
    """

    def role_checker(user: UserDep):
        if user["role"] != required_role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied for role: {user['role']}",
            )
        return user

    return role_checker


AdminRoleDep = Annotated[User, Depends(require_role(Role.ADMIN))]
UserRoleDep = Annotated[User, Depends(require_role(Role.USER))]
GuestRoleDep = Annotated[User, Depends(require_role(Role.GUEST))]
