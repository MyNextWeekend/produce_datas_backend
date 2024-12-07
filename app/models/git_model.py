from .base import Base
from sqlmodel import Field


class ProjectInfo(Base, table=True):
    """
    项目信息表
    """
    repository_name: str = Field(index=True, description="项目名称")
    repository_url: str = Field(description="项目地址")
    description: str | None = Field(default=None, description="项目描述")


class ArgsConf(Base, table=True):
    """
    参数配置
    """
    pass


class CaseFunc(Base, table=True):
    """
    解析文件 用例表
    """
    pass


class TaskInfo(Base, table=True):
    """
    任务执行信息
    """
    pass
