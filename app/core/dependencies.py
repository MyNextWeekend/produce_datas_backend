from collections.abc import Generator
from enum import Enum
from typing import Annotated, Self

from fastapi import Depends, Header
from sqlalchemy import create_engine
from sqlmodel import Session

from app.core.config import settings
from app.core.exception import BusinessException, ErrorEnum
from app.services.user_service import UserService

engine = create_engine(str(settings.mysql.uri), echo=True, pool_size=8, pool_recycle=60 * 30)


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


def get_user_by_token(token: HeaderDep) -> UserService:
    """
    校验 请求头 header 中的 token
    并且从数据库获取 用户信息
    """
    user = UserService.from_token(token)
    # 续 token 有效时间
    user.refresh()
    return user


UserDep = Annotated[UserService, Depends(get_user_by_token)]


class Role(int, Enum):
    ADMIN = 1
    USER = 2
    GUEST = 3

    @classmethod
    def from_role(cls, role_int: int) -> Self:
        for role in Role:
            if role.value == role_int:
                return role
        raise BusinessException.new(ErrorEnum.INVALID_ROLE)


def require_role(required_role: Role):
    """
    管理 api 特定权限的用户访问
    """

    def inner(user: UserDep) -> UserService:
        # 大于指定的权限即可（数值越小，权限越大）
        if Role.from_role(user.role).value > required_role.value:
            raise BusinessException.new(ErrorEnum.PERMISSION_DENIED)
        return user

    return inner


AdminRoleDep = Annotated[UserService, Depends(require_role(Role.ADMIN))]
UserRoleDep = Annotated[UserService, Depends(require_role(Role.USER))]
GuestRoleDep = Annotated[UserService, Depends(require_role(Role.GUEST))]
