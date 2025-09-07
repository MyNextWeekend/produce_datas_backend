from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InsertReq(BaseModel):
    name: str  # 名称
    code: str  # 接口唯一code
    method: str  # HTTP 请求方法:get,post
    domain_code: str  # 域名code
    path: str  # 接口路径
    description: Optional[str] = None  # 接口描述
    is_active: Optional[int] = None  # 是否启用


class UpdateReq(BaseModel):
    id: int
    name: Optional[str] = None  # 名称
    code: Optional[str] = None  # 接口唯一code
    method: Optional[str] = None  # HTTP 请求方法:get,post
    domain_code: Optional[str] = None  # 域名code
    path: Optional[str] = None  # 接口路径
    description: Optional[str] = None  # 接口描述
    is_active: Optional[int] = None  # 是否启用


class SearchVo(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None  # 名称
    code: Optional[str] = None  # 接口唯一code
    method: Optional[str] = None  # HTTP 请求方法:get,post
    domain_code: Optional[str] = None  # 域名code
    path: Optional[str] = None  # 接口路径
    description: Optional[str] = None  # 接口描述
    is_active: Optional[int] = None  # 是否启用
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
