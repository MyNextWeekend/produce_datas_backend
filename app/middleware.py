import time
import uuid

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.utils.log_utils import Log, trace_id

logger = Log().get_logger()


class UseTimeMiddleware(BaseHTTPMiddleware):
    """ 计算耗时中间件"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """ 请求耗时 """
        start_time = time.time()
        # 调用下一个中间件或路由处理函数
        result = await call_next(request)
        process_time = time.time() - start_time
        result.headers["X-Process-Time"] = f"{process_time * 1000:.2f}"
        return result

class TraceIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """请求头获取 trace_id 并设置到上下文中，最终返回用户"""
        trace_id_header = request.headers.get('X-Trace-Id', str(uuid.uuid4()).replace("-", ""))
        trace_id.set(trace_id_header)
        response = await call_next(request)
        response.headers['X-Trace-Id'] = trace_id_header
        return response


def register_middleware_handle(server: FastAPI):
    logger.info("register middleware handle...")
    # 添加 trace_id 中间件
    server.add_middleware(TraceIDMiddleware)
    # 添加耗时请求中间件
    server.add_middleware(UseTimeMiddleware)
    # 测试
    # server.add_middleware(TestMiddleware)
    logger.info("register middleware handle successfully.")
