from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SearchVo(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    method: Optional[str] = None
    domain_code: Optional[str] = None
    path: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
