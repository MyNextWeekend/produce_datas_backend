# =====================================================================
# ========== Automatically generate file, do not modify it ! ==========
# =====================================================================
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Column, DateTime, Index, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import MEDIUMBLOB, TINYINT
from sqlmodel import Field, SQLModel

class CustomParameter(SQLModel, table=True):
    __tablename__ = 'custom_parameter'
    __table_args__ = {'comment': '存放自定义参数信息'}

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, primary_key=True))
    key_name: str = Field(sa_column=Column('key_name', String(255), comment='参数键'))
    value: str = Field(sa_column=Column('value', Text, comment='参数值'))
    description: Optional[str] = Field(default=None, sa_column=Column('description', Text, comment='参数描述'))
    created_at: Optional[datetime] = Field(default=None, sa_column=Column('created_at', DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间'))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column('updated_at', DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间'))


class DatabaseInfo(SQLModel, table=True):
    __tablename__ = 'database_info'
    __table_args__ = {'comment': '数据库相关信息'}

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, primary_key=True))
    name: str = Field(sa_column=Column('name', String(255), comment='数据库标识名'))
    environment: str = Field(sa_column=Column('environment', String(32), comment='环境标识:sit,uat'))
    host: str = Field(sa_column=Column('host', String(255), comment='数据库主机地址'))
    port: int = Field(sa_column=Column('port', Integer, comment='数据库端口'))
    username: str = Field(sa_column=Column('username', String(255), comment='用户名'))
    password: str = Field(sa_column=Column('password', String(255), comment='密码（加密存储）'))
    db_name: str = Field(sa_column=Column('db_name', String(255), comment='数据库名'))
    description: Optional[str] = Field(default=None, sa_column=Column('description', Text, comment='描述'))
    created_at: Optional[datetime] = Field(default=None, sa_column=Column('created_at', DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间'))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column('updated_at', DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间'))


class Domain(SQLModel, table=True):
    __table_args__ = (
        Index('code_environment_unique', 'code', 'environment', unique=True),
        {'comment': '接口域名表'}
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, primary_key=True))
    name: str = Field(sa_column=Column('name', String(255), comment='名称'))
    code: str = Field(sa_column=Column('code', String(255), comment='接口唯一code'))
    environment: str = Field(sa_column=Column('environment', String(32), comment='环境标识:sit,uat'))
    domain: str = Field(sa_column=Column('domain', String(255), comment='域名'))
    description: Optional[str] = Field(default=None, sa_column=Column('description', Text, comment='接口描述'))
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
    domain_code: str = Field(sa_column=Column('domain_code', String(32), comment='域名code'))
    path: str = Field(sa_column=Column('path', String(255), comment='接口路径'))
    description: Optional[str] = Field(default=None, sa_column=Column('description', Text, comment='接口描述'))
    is_active: Optional[int] = Field(default=None, sa_column=Column('is_active', TINYINT(1), server_default=text("'1'"), comment='是否启用'))
    created_at: Optional[datetime] = Field(default=None, sa_column=Column('created_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间'))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column('updated_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间'))


class Report(SQLModel, table=True):
    __table_args__ = {'comment': '存放测试报告信息'}

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, primary_key=True))
    task_id: int = Field(sa_column=Column('task_id', BigInteger, comment='任务 ID'))
    version: int = Field(sa_column=Column('version', BigInteger, comment='版本号'))
    status: int = Field(sa_column=Column('status', Integer, comment='执行状态'))
    created_at: Optional[datetime] = Field(default=None, sa_column=Column('created_at', DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='执行时间'))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column('updated_at', DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间'))


class ReportDetail(SQLModel, table=True):
    __tablename__ = 'report_detail'
    __table_args__ = {'comment': '存储用例执行产生的日志或截图信息'}

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, primary_key=True))
    report_id: int = Field(sa_column=Column('report_id', BigInteger, comment='测试报告 ID'))
    content_type: str = Field(sa_column=Column('content_type', String(50), comment='内容类型（如日志、截图）'))
    content: Optional[bytes] = Field(default=None, sa_column=Column('content', MEDIUMBLOB, comment='内容数据（如日志文本、截图文件）'))
    created_at: Optional[datetime] = Field(default=None, sa_column=Column('created_at', DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间'))


class Repository(SQLModel, table=True):
    __table_args__ = {'comment': '存放 Git 仓库地址'}

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, primary_key=True))
    name: str = Field(sa_column=Column('name', String(255), comment='仓库名称'))
    url: str = Field(sa_column=Column('url', Text, comment='Git 仓库地址'))
    branch: Optional[str] = Field(default=None, sa_column=Column('branch', String(255), server_default=text("'main'"), comment='分支'))
    description: Optional[str] = Field(default=None, sa_column=Column('description', Text, comment='描述'))
    created_at: Optional[datetime] = Field(default=None, sa_column=Column('created_at', DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间'))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column('updated_at', DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间'))


class RepositoryDetail(SQLModel, table=True):
    __tablename__ = 'repository_detail'
    __table_args__ = {'comment': '存放 Git 仓库地址'}

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, primary_key=True))
    repository_id: int = Field(sa_column=Column('repository_id', BigInteger, comment='仓库id'))
    url: str = Field(sa_column=Column('url', Text, comment='Git 仓库地址'))
    branch: str = Field(sa_column=Column('branch', String(255), comment='分支'))
    version: Optional[int] = Field(default=None, sa_column=Column('version', BigInteger, comment='版本号'))
    is_latest: Optional[int] = Field(default=None, sa_column=Column('is_latest', TINYINT(1), server_default=text("'0'"), comment='是否为最新版本'))
    task_num: Optional[int] = Field(default=None, sa_column=Column('task_num', Integer, server_default=text("'0'"), comment='任务数量'))
    description: Optional[str] = Field(default=None, sa_column=Column('description', Text, comment='描述'))
    created_at: Optional[datetime] = Field(default=None, sa_column=Column('created_at', DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间'))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column('updated_at', DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间'))


class Schedule(SQLModel, table=True):
    __table_args__ = {'comment': '存放任务的定时信息'}

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, primary_key=True))
    task_id: int = Field(sa_column=Column('task_id', BigInteger, comment='任务 ID'))
    cron_expression: str = Field(sa_column=Column('cron_expression', String(255), comment='CRON 表达式'))
    enabled: Optional[int] = Field(default=None, sa_column=Column('enabled', TINYINT(1), server_default=text("'1'"), comment='是否启用'))
    created_at: Optional[datetime] = Field(default=None, sa_column=Column('created_at', DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间'))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column('updated_at', DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间'))


class Task(SQLModel, table=True):
    __table_args__ = {'comment': '存放任务信息'}

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, primary_key=True))
    version: int = Field(sa_column=Column('version', BigInteger, comment='版本号'))
    file_path: str = Field(sa_column=Column('file_path', String(255), comment='文件路径'))
    func_name: str = Field(sa_column=Column('func_name', String(64), comment='方法名称'))
    cron_expression: str = Field(sa_column=Column('cron_expression', String(255), comment='CRON 表达式'))
    description: Optional[str] = Field(default=None, sa_column=Column('description', Text, comment='描述'))
    created_at: Optional[datetime] = Field(default=None, sa_column=Column('created_at', DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间'))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column('updated_at', DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间'))


class User(SQLModel, table=True):
    __table_args__ = {'comment': '用户信息'}

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, primary_key=True))
    username: str = Field(sa_column=Column('username', String(50), comment='账号'))
    password: str = Field(sa_column=Column('password', String(50), comment='密码'))
    created_at: Optional[datetime] = Field(default=None, sa_column=Column('created_at', DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间'))
