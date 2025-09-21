from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar("T", bound=BaseModel)


class BaseVo(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # 把 snake_case 字段映射为 camelCase 的别名（用于接收/输出）
        populate_by_name=True  # 允许用字段名（snake_case）直接填充（可选）
    )


class SortOrderEnum(str, Enum):
    """
    排序字段
    """
    asc: str = "asc"
    desc: str = "desc"


class PageReq(BaseVo, Generic[T]):
    """
    统一的分页查询结构体
    """
    page: int
    page_size: int
    sort_by: Optional[str] = None
    sort_order: Optional[SortOrderEnum] = None
    filter: Optional[T] = None


class IdReq(BaseVo):
    id: int


class StatisticResp(BaseVo):
    total: int
