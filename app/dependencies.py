from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from .models import engine


def get_query_token():
    print("get_query_token")


def get_token_header():
    print("get_token_header")


def get_session() -> Generator[Session, None, None]:
    """
    为每个请求yield提供一个新的Session
    :return: 会话
    """
    with Session(engine) as session:
        yield session


# 为了简化代码
SessionDep = Annotated[Session, Depends(get_session)]
