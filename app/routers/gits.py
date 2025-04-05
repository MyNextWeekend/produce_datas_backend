import datetime

from fastapi import APIRouter

from app import schemas
from app.dependencies import SessionDep
from app.models import ProjectInfo
from app.schemas import Response
from app.utils import LogUtil

logger = LogUtil().get_logger()

router = APIRouter(prefix="/git", tags=["git操作"])  # 接口文档中的标签


@router.post("/project/add", summary="新增git配置", response_model=Response[ProjectInfo])
async def project_add(project: schemas.Repository, session: SessionDep) -> Response[ProjectInfo]:
    # 校验仓库地址是否有效
    info = ProjectInfo(
        repository_name=project.repository_name,
        repository_url=project.repository_url,
        description=project.description,
        create_by="admin",
        create_time=datetime.datetime.now(),
        update_by="admin",
        update_time=datetime.datetime.now(),
    )
    # session.add(info)
    # session.commit()
    # session.flush()
    logger.info("good")
    # 存入数据库
    return schemas.Response[ProjectInfo].ok(data=info)


@router.post("/project/modify", summary="修改git配置")
async def project_modify(project: schemas.Repository, session: SessionDep):
    pass


@router.post("/project/list", summary="修改git配置")
async def project_list():
    # 校验仓库地址是否有效
    # 修改最新的仓库地址 带权限条件一起
    pass


# @router.post("/config/get", summary="查询git配置")
# def read_heroes(
#         session: SessionDep,
#         offset: int = 0,
#         limit: Annotated[int, Query(le=100)] = 100) -> list[Hero]:
#     heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
#     return heroes


@router.post("/repository/clone", summary="同步远程仓库")
async def git_clone():
    # 校验仓库地址是否有效
    # clone仓库
    # 把仓库文件地址写入数据库
    # 解析仓库
    # 写入数据库
    pass
