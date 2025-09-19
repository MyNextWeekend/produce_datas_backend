
from fastapi import APIRouter

from app.core.exception import Resp

router = APIRouter(tags=["测试"])


@router.get("/hello", summary="测试接口")
async def hello() -> Resp[str]:
    return Resp.success("Hello World!")
