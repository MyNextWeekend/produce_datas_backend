from fastapi import APIRouter

router = APIRouter(prefix="/task")


@router.post("/exec")
async def exec_task():
    print("exec_task")
