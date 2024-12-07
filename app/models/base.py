import datetime

from sqlmodel import Field, SQLModel, create_engine

from ..config import settings

engine = create_engine(str(settings.sqlmodel_database_uri), echo=True, pool_size=8, pool_recycle=60 * 30)


class Base(SQLModel):
    """
    表基类，提供基础字段配置
    """
    id: int = Field(primary_key=True, index=True, default=None, description="表主键")
    create_by: str | None = Field(description="创建人")
    create_time: datetime.datetime | None = Field(description="创建时间")
    update_by: str | None = Field(description="更新人")
    update_time: datetime.datetime | None = Field(description="更新时间")
    is_deleted: int | None = Field(default=0, description="删除标识")


def create_table():
    """通过模型创建表结构"""
    SQLModel.metadata.create_all(engine)
