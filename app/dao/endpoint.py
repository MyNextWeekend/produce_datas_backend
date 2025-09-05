from typing import List

from sqlmodel import Session, select

from app.models.first_model import Endpoint
from app.vo import Query
from app.vo.endpoint_vo import SearchVo


class EndpointDao:

    @classmethod
    def query(cls, session: Session, query: Query[SearchVo]) -> List[Endpoint]:
        stmt = select(Endpoint)
        if query.data is not None:
            if query.data.id is not None:
                stmt = stmt.where(Endpoint.id == query.data.id)
            if query.data.name is not None:
                stmt = stmt.where(Endpoint.name == query.data.name)
            if query.data.code is not None:
                stmt = stmt.where(Endpoint.code == query.data.code)
            if query.data.method is not None:
                stmt = stmt.where(Endpoint.method == query.data.method)
            if query.data.domain_code is not None:
                stmt = stmt.where(Endpoint.domain_code == query.data.domain_code)
            if query.data.path is not None:
                stmt = stmt.where(Endpoint.path == query.data.path)
            if query.data.description is not None:
                stmt = stmt.where(Endpoint.description == query.data.description)
            if query.data.is_active is not None:
                stmt = stmt.where(Endpoint.is_active == query.data.is_active)
        return session.exec(stmt.offset((query.page - 1) * query.page_size).limit(query.page_size)).all()
