from pydantic import BaseModel


class Repository(BaseModel):
    id: int | None = None
    repository_name: str
    repository_url: str
    description: str | None = None
