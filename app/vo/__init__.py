from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Query(BaseModel, Generic[T]):
    page: int
    page_size: int
    data: Optional[T]
