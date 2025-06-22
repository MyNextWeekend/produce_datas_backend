import importlib
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.exception import register_exception_handle
from app.middleware import register_middleware_handle
from app.utils.log_utils import Log

logger = Log().get_logger()


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

# 注册中间件
register_middleware_handle(app)

# 添加自定义异常
register_exception_handle(app)


def register_routers(server: FastAPI, routers_path: Path):
    """
    动态注册指定目录中的所有路由模块。
    Args:
        server (FastAPI): FastAPI 应用实例。
        routers_path (Path): 路由文件夹路径。
    """
    if not routers_path.exists() or not routers_path.is_dir():
        raise FileNotFoundError(f"路由目录不存在: {routers_path}")

    for file in routers_path.rglob("*.py"):
        if file.name == "__init__.py":
            logger.info(f"{file} skipped")
            continue

        # 构造模块名，例如 'routers.user'
        relative_path = file.relative_to(routers_path.parent)
        module_name = ".".join(relative_path.with_suffix("").parts)

        try:
            module = importlib.import_module(module_name)
            # 检查并注册 router 对象
            if hasattr(module, "router"):
                server.include_router(module.router)
                logger.info(f"register router from {module_name} successfully")
            else:
                logger.warning(f"not found router from {module_name}, skip...")
        except Exception as e:
            logger.error(f"import module failed: {e}", exc_info=True)


# 自动注册路由
register_routers(app, Path(__file__).parent.joinpath("routers"))

# 手动启动命令
# uv run uvicorn app.main:app --host 0.0.0.0 --port 8080
if __name__ == '__main__':
    import uvicorn

    # 断点调试使用
    uvicorn.run(app="main:app", host='0.0.0.0', port=8080, reload=True)
