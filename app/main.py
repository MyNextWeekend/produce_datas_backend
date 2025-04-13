from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import endpoint
from app.utils.log_utils import Log

logger = Log().get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    可以设置服务启动之后 自动创建数据库表
    """
    logger.info("web init...")
    # create_table()  # 启动服务器做一些事情
    yield
    pass  # 关闭服务后做一些事情
    logger.info("web stopped !!!")


app = FastAPI(lifespan=lifespan)

# 注册中间件
# register_middleware_handle(app)

# 子路由
app.include_router(endpoint.router)

# 启动命令
# uv run uvicorn app.main:app --host 0.0.0.0 --port 8080
