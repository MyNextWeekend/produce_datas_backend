from datetime import datetime
from typing import Optional

from pydantic import Field

from app.vo import BaseVo


class InsertReq(BaseVo):
    key_name: str = Field(..., min_length=2, description="参数键")
    value: str = Field(..., min_length=2, description="参数值")
    description: Optional[str] = Field(None, description="参数描述")


class UpdateReq(BaseVo):
    id: int = Field(..., gt=0, description="id")
    key_name: Optional[str] = Field(None, min_length=2, description="参数键")
    value: Optional[str] = Field(None, min_length=2, description="参数值")
    description: Optional[str] = Field(None, description="参数描述")


class SearchVo(BaseVo):
    id: Optional[int] = None
    key_name: Optional[str] = None  # 参数键
    value: Optional[str] = None  # 参数值
    description: Optional[str] = None  # 参数描述
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StatisticResp(BaseVo):
    total: int
