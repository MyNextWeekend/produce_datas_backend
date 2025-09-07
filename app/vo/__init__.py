from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class SortOrderEnum(str, Enum):
    """
    排序字段
    """
    asc: str = "asc"
    desc: str = "desc"


class PageReq(BaseModel, Generic[T]):
    """
    统一的分页查询结构体
    """
    page: int
    page_size: int
    sort_by: Optional[str] = None
    sort_order: Optional[SortOrderEnum] = None
    filter: Optional[T] = None


class IdReq(BaseModel):
    id: int
