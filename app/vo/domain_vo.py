from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InsertVO(BaseModel):
    name: str  # 名称
    code: str  # 接口唯一code
    environment: str  # 环境标识:sit,uat
    domain: str  # 域名
    description: Optional[str]  # 接口描述


class UpdateVO(BaseModel):
    id: int
    name: Optional[str] = None  # 名称
    code: Optional[str] = None  # 接口唯一code
    environment: Optional[str] = None  # 环境标识:sit,uat
    domain: Optional[str] = None  # 域名
    description: Optional[str] = None  # 接口描述


class SearchVO(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None  # 名称
    code: Optional[str] = None  # 接口唯一code
    environment: Optional[str] = None  # 环境标识:sit,uat
    domain: Optional[str] = None  # 域名
    description: Optional[str] = None  # 接口描述
    created_at: Optional[datetime] = None  # 创建时间
    updated_at: Optional[datetime] = None  # 更新时间
