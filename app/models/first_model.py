# =====================================================================
# ========== Automatically generate file, do not modify it ! ==========
# =====================================================================
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Column, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlmodel import Field, SQLModel

class Domain(SQLModel, table=True):
    __table_args__ = (
        Index('name_environment_unique', 'name', 'environment', unique=True),
        {'comment': '接口域名表'}
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, primary_key=True))
    name: str = Field(sa_column=Column('name', String(255), comment='名称'))
    environment: str = Field(sa_column=Column('environment', String(32), comment='环境标识:sit,uat'))
    domain: str = Field(sa_column=Column('domain', String(255), comment='域名'))
    created_at: Optional[datetime] = Field(default=None, sa_column=Column('created_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间'))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column('updated_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间'))


class Endpoint(SQLModel, table=True):
    __table_args__ = (
        Index('code_unique', 'code', unique=True),
        {'comment': '接口基本信息表'}
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, primary_key=True))
    name: str = Field(sa_column=Column('name', String(255), comment='名称'))
    code: str = Field(sa_column=Column('code', String(255), comment='接口唯一code'))
    method: str = Field(sa_column=Column('method', String(32), comment='HTTP 请求方法:get,post'))
    path: str = Field(sa_column=Column('path', String(255), comment='接口路径'))
    description: Optional[str] = Field(default=None, sa_column=Column('description', Text, comment='接口描述'))
    is_active: Optional[int] = Field(default=None, sa_column=Column('is_active', TINYINT(1), server_default=text("'1'"), comment='是否启用'))
    created_at: Optional[datetime] = Field(default=None, sa_column=Column('created_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间'))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column('updated_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间'))
