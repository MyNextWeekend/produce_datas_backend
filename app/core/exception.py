import traceback
from enum import Enum
from typing import Generic, Optional, Self, TypeVar

from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.utils.log_utils import logger

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


class ErrorEnum(Enum):
    # 客户端错误
    BAD_REQUEST = (901, "请求参数错误或不符合要求")
    INVALID_CREDENTIALS = (902, "用户名或者密码错误")
    UNAUTHORIZED = (903, "需要用户认证或认证已失效")
    FORBIDDEN = (904, "没有访问该资源的权限")
    NOT_FOUND = (905, "请求的资源不存在")
    CONFLICT = (906, "请求冲突，例如资源已存在")
    TOO_MANY_REQUESTS = (907, "请求过于频繁，请稍后重试")
    PAYLOAD_TOO_LARGE = (908, "请求数据过大")

    # 服务端错误
    INTERNAL_SERVER_ERROR = (999, "服务器内部出现异常")
    NOT_IMPLEMENTED = (910, "接口未实现或未开放")
    BAD_GATEWAY = (911, "网关错误")
    SERVICE_UNAVAILABLE = (912, "服务暂时不可用，请稍后重试")
    GATEWAY_TIMEOUT = (913, "网关超时")

    # 业务相关错误（可根据你的系统扩展）
    USER_NOT_FOUND = (920, "用户不存在")
    USER_DISABLED = (921, "用户已被禁用")
    TOKEN_EXPIRED = (922, "登录凭证已过期")
    TOKEN_INVALID = (923, "登录凭证无效")
    PERMISSION_DENIED = (924, "权限不足")
    RESOURCE_LOCKED = (925, "资源被锁定，无法修改")
    VALIDATION_ERROR = (926, "数据校验失败")
    OPERATION_FAILED = (927, "操作失败，请重试")
    INVALID_ROLE = (928, "不合法的角色")

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


class BusinessException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    @classmethod
    def new(cls, error: ErrorEnum):
        return BusinessException(error.code, error.message)


def register_exception_handle(server: FastAPI):
    logger.info("register exception handle...")

    @server.exception_handler(BusinessException)
    async def http_business_exception_handler(_: Request, exc: BusinessException):
        logger.warning(traceback.format_exc())  # 记录异常堆栈,自定义异常使用 warning 级别
        return JSONResponse(status_code=200, content=Resp(code=exc.code, message=exc.message).model_dump())

    @server.exception_handler(Exception)
    async def http_exception_handler(_request: Request, _exc: Exception):
        return JSONResponse(status_code=500, content=Resp(message="服务内部异常").model_dump())

    logger.info("register exception handle successfully.")
