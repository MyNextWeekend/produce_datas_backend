from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import update
from sqlmodel import Session, SQLModel, asc, desc, select

from app.vo import PageReq, SortOrderEnum

T = TypeVar("T", bound=SQLModel)
E = TypeVar("E", bound=BaseModel)


class Dao(Generic[T]):
    def __init__(self, session: Session, table_model: Type[T]):
        self.session = session
        self.table_model = table_model

    def query_by_id(self, obj_id: int) -> Optional[T]:
        return self.session.get(self.table_model, obj_id)

    def query(self, parm: PageReq[E] = None) -> List[T]:
        stmt = select(self.table_model)
        filter_obj = parm.filter
        # 动态组装查询条件
        if filter_obj:
            for field, value in parm.filter.model_dump(exclude_none=True).items():
                if hasattr(self.table_model, field):
                    stmt = stmt.where(getattr(self.table_model, field) == value)
        # 分页查询
        stmt = stmt.limit(parm.page_size).offset((parm.page - 1) * parm.page_size)
        # 排序字段
        if parm.sort_by:
            if parm.sort_order and parm.sort_order == SortOrderEnum.desc:
                stmt = stmt.order_by(desc(parm.sort_by))
            else:
                stmt = stmt.order_by(asc(parm.sort_by))
        return self.session.exec(stmt).all()

    def update_by_id(self, parm: E, commit: bool = True) -> Optional[T]:
        table_id = parm.id
        if not table_id:
            raise ValueError("table_id is required")
        values = parm.model_dump(exclude_none=True, exclude={"id"})
        stmt = (
            update(self.table_model)
            .where(self.table_model.id == table_id)
            .values(**values)
        )
        self.session.exec(stmt)
        if commit:
            self.session.commit()
        return True

    def insert(self, obj: T, commit: bool = True) -> T:
        self.session.add(obj)
        if commit:
            self.session.commit()
            self.session.refresh(obj)
        return obj

    def delete_by_id(self, table_id: int, commit: bool = True) -> bool:
        obj = self.query_by_id(table_id)
        if not obj:
            return False
        self.session.delete(obj)
        if commit:
            self.session.commit()
        return True
