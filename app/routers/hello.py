import asyncio

from fastapi import APIRouter

from app.core.exception import Resp
from app.utils.log_utils import logger

router = APIRouter(prefix="/hello", tags=["测试"])


async def do_something():
    logger.info("do something start")
    await asyncio.sleep(1)
    logger.info("do something end...")


@router.get("/", summary="测试接口")
async def hello() -> Resp[str]:
    logger.info("func hello start")
    await do_something()
    logger.info("func hello end...")
    return Resp.success("Hello World!")
