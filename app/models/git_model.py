from sqlmodel import Field, SQLModel


class ProjectInfo(SQLModel, table=True):
    """
    项目信息表
    """

    id: int = Field(default=None, primary_key=True)
    repository_name: str = Field(index=True, description="项目名称")
    repository_url: str = Field(description="项目地址")
    description: str | None = Field(default=None, description="项目描述")


class ArgsConf(SQLModel, table=True):
    """
    参数配置
    """

    id: int = Field(default=None, primary_key=True)
    pass


class CaseFunc(SQLModel, table=True):
    """
    解析文件 用例表
    """

    id: int = Field(default=None, primary_key=True)
    pass


class TaskInfo(SQLModel, table=True):
    """
    任务执行信息
    """

    id: int = Field(default=None, primary_key=True)
    pass
