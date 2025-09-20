from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlmodel import SQLModel


class CamelModel(SQLModel):
    """
    所有生成的模型都继承此类，自动支持 snake_case -> camelCase
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
