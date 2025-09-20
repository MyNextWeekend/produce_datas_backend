from typing import Optional

from sqlalchemy import Select
from sqlmodel import Session

from app.dao import Dao
from app.models.first_model import Endpoint
from app.vo.endpoint_vo import SearchVo


class EndpointDao(Dao[Endpoint]):

    def __init__(self, session: Session):
        super().__init__(session, Endpoint)

    def apply_filters(self, stmt: Select, filter_model: Optional[SearchVo]) -> Select:
        if filter_model:
            if filter_model.id:
                stmt = stmt.where(Endpoint.id == filter_model.id)
            if filter_model.name:
                stmt = stmt.where(Endpoint.name == filter_model.name)
            if filter_model.code:
                stmt = stmt.where(Endpoint.code == filter_model.code)
            if filter_model.method:
                stmt = stmt.where(Endpoint.method == filter_model.method)
            if filter_model.domain_code:
                stmt = stmt.where(Endpoint.domain_code == filter_model.domain_code)
            if filter_model.path:
                stmt = stmt.where(Endpoint.path == filter_model.path)
            if filter_model.description:
                stmt = stmt.where(Endpoint.description == filter_model.description)
            if filter_model.is_active:
                stmt = stmt.where(Endpoint.is_active == filter_model.is_active)
        return stmt
