from typing import Optional

from pydantic import BaseModel


class CaseInfo(BaseModel):
    file: str
    method: Optional[str] = None
