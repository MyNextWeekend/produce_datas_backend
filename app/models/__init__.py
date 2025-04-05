import datetime

from sqlmodel import Field, SQLModel, create_engine

from app.config import settings

from .git_model import *  # noqa

engine = create_engine(str(settings.sqlmodel_database_uri), echo=True, pool_size=8, pool_recycle=60 * 30)


# def create_table():
#     """通过模型创建表结构"""
#     SQLModel.metadata.create_all(engine)
