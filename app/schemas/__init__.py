from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel

from .git_schema import *  # noqa: F403

T = TypeVar("T")


# 定义响应统一结构体
class Response(BaseModel, Generic[T]):
    code: int = 0
    message: str = ""
    data: T

    @classmethod
    def ok(cls, data: T) -> Response[T]:
        return Response(data=data)

    @classmethod
    def error(cls, code: int = 666, message: str = "", data: T = None) -> Response[T]:
        return Response(code=code, message=message, data=data)
