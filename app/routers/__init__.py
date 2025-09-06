import importlib
from pathlib import Path

from fastapi import FastAPI

from app.core.config import settings
from app.utils.log_utils import logger


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
        relative_path = file.relative_to(settings.root_dir)
        module_name = ".".join(relative_path.with_suffix("").parts)

        try:
            module = importlib.import_module(module_name)
            # 检查并注册 router 对象
            if hasattr(module, "router"):
                server.include_router(module.router, prefix=settings.prefix)
                logger.info(f"register router from {module_name} successfully")
            else:
                logger.warning(f"not found router from {module_name}, skip...")
        except Exception as e:
            logger.error(f"import module failed: {e}", exc_info=True)
