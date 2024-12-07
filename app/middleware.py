import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class UseTimeMiddleware(BaseHTTPMiddleware):
    """ 计算耗时中间件"""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        """ 请求耗时 """
        start_time = time.time()
        # 调用下一个中间件或路由处理函数
        result = await call_next(request)
        process_time = time.time() - start_time
        result.headers["X-Process-Time"] = str(process_time)
        return result


def register_middleware_handle(server: FastAPI):
    # 添加token验证中间件
    # server.add_middleware(TokenMiddleware)
    # 添加耗时请求中间件
    server.add_middleware(UseTimeMiddleware)
    # 测试
    # server.add_middleware(TestMiddleware)
