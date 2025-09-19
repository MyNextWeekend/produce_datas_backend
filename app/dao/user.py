from typing import Optional

from sqlmodel import Session, select

from app.dao import Dao
from app.models.first_model import User


class UserDao(Dao[User]):

    def __init__(self, session: Session):
        super().__init__(session, User)

    def query_by_username(self, username: str) -> Optional[User]:
        statement = select(self.table_model).where(User.username == username)
        return self.session.exec(statement).first()
