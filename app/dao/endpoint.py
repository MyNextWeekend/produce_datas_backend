from typing import List

from sqlmodel import Session, select

from app.dao import Dao
from app.models.first_model import Endpoint
from app.vo import PageReq
from app.vo.endpoint_vo import SearchVo


class EndpointDao(Dao[Endpoint]):

    def __init__(self, session: Session):
        super().__init__(session, Endpoint)

    def list(self, session: Session, parm: PageReq[SearchVo]) -> List[Endpoint]:
        stmt = select(Endpoint)
        if parm.filter is not None:
            if parm.filter.id is not None:
                stmt = stmt.where(Endpoint.id == parm.filter.id)
            if parm.filter.name is not None:
                stmt = stmt.where(Endpoint.name == parm.filter.name)
            if parm.filter.code is not None:
                stmt = stmt.where(Endpoint.code == parm.filter.code)
            if parm.filter.method is not None:
                stmt = stmt.where(Endpoint.method == parm.filter.method)
            if parm.filter.domain_code is not None:
                stmt = stmt.where(Endpoint.domain_code == parm.filter.domain_code)
            if parm.filter.path is not None:
                stmt = stmt.where(Endpoint.path == parm.filter.path)
            if parm.filter.description is not None:
                stmt = stmt.where(Endpoint.description == parm.filter.description)
            if parm.filter.is_active is not None:
                stmt = stmt.where(Endpoint.is_active == parm.filter.is_active)
        return session.exec(stmt.offset((parm.page - 1) * parm.page_size).limit(parm.page_size)).all()
