from datetime import datetime
from typing import Optional

from app.vo import BaseVo


class InsertReq(BaseVo):
    name: str  # 名称
    code: str  # 接口唯一code
    method: str  # HTTP 请求方法:get,post
    domain_code: str  # 域名code
    path: str  # 接口路径
    description: Optional[str] = None  # 接口描述
    is_active: Optional[int] = None  # 是否启用


class UpdateReq(BaseVo):
    id: int
    name: Optional[str] = None  # 名称
    code: Optional[str] = None  # 接口唯一code
    method: Optional[str] = None  # HTTP 请求方法:get,post
    domain_code: Optional[str] = None  # 域名code
    path: Optional[str] = None  # 接口路径
    description: Optional[str] = None  # 接口描述
    is_active: Optional[int] = None  # 是否启用


class SearchVo(BaseVo):
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
