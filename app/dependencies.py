from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session

from app.config import settings


def get_query_token():
    print("get_query_token")


def get_token_header():
    print("get_token_header")


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
