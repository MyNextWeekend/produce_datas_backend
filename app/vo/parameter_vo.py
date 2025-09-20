from datetime import datetime
from typing import Optional

from app.vo import BaseVo


class InsertReq(BaseVo):
    key_name: str = None  # 参数键
    value: str = None  # 参数值
    description: Optional[str] = None  # 参数描述


class UpdateReq(BaseVo):
    id: int = None
    key_name: Optional[str] = None  # 参数键
    value: Optional[str] = None  # 参数值
    description: Optional[str] = None  # 参数描述


class SearchVo(BaseVo):
    id: Optional[int] = None
    key_name: Optional[str] = None  # 参数键
    value: Optional[str] = None  # 参数值
    description: Optional[str] = None  # 参数描述
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
