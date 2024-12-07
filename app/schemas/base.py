from typing import Generic, Self, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


# 定义响应统一结构体
class Response(BaseModel, Generic[T]):
    code: int = 0
    message: str = ""
    data: T

    @classmethod
    def ok(cls, data: T) -> Self:
        return Response(data=data)

    @classmethod
    def error(cls, code: int = 666, message: str = "", data: T = None) -> Self:
        return Response(code=code, message=message, data=data)
