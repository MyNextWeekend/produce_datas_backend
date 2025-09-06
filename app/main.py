from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.exception import register_exception_handle
from app.core.middleware import register_middleware_handle
from app.routers import register_routers
from app.utils.log_utils import logger


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    可以设置服务启动之后 自动创建数据库表
    """
    logger.info("web init...")
    # create_table()  # 启动服务器做一些事情
    yield
    # 关闭服务后做一些事情  pass
    logger.info("web stopped !!!")


app = FastAPI(lifespan=lifespan)

register_middleware_handle(app)  # 注册中间件
register_exception_handle(app)  # 注册自定义异常
register_routers(app, settings.root_dir.joinpath("app", "routers"))  # 注册路由

# 手动启动命令
# uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
if __name__ == '__main__':
    import uvicorn

    # 断点调试使用
    uvicorn.run(app="main:app", host='0.0.0.0', port=8080, reload=True)
