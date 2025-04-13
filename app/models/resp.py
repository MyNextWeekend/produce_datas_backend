from typing import Generic, Optional, Self, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Resp(BaseModel, Generic[T]):
    code: int = 0
    message: str = "OK"
    data: Optional[T] = None

    @classmethod
    def success(cls, data: T) -> Self:
        return cls(data=data)

    @classmethod
    def fail(cls, code: int = -1, message: str = "fail", data: T = None) -> Self:
        return cls(code=code, message=message, data=data)
