from contextlib import asynccontextmanager

from fastapi import FastAPI

from .routers import gits, tasks
from .utils import LogUtil

logger = LogUtil().get_logger()


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
app.include_router(gits.router, tags=["项目操作"])  # 接口文档中的标签
app.include_router(tasks.router, tags=["任务操作"])
