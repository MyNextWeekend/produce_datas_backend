from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class InsertReq(BaseModel):
    username: str  # 账号
    password: str  # 密码
    email: str  # 邮箱
    role: int  # 角色


class UpdateReq(BaseModel):
    id: int = None
    username: Optional[str] = None  # 账号
    password: Optional[str] = None  # 密码
    email: Optional[str] = None  # 邮箱
    role: Optional[int] = None  # 角色
    is_active: Optional[int] = None


class SearchVo(BaseModel):
    id: Optional[int] = None  # id
    username: Optional[str] = None  # 账号
    password: Optional[str] = None  # 密码
    email: Optional[str] = None  # 邮箱
    role: Optional[str] = None  # 角色
    is_active: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
