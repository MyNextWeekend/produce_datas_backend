from typing import Self

from app.core.config import settings
from app.core.dependencies import SessionDep
from app.core.exception import BusinessException, ErrorEnum
from app.dao import Dao
from app.models.first_model import User
from app.utils.redis_utils import redis_client
from app.utils.snow_utils import snowflake_generator


class UserService:
    TOKEN_EXPIRE_SECONDS = 60 * 60  # 1h

    def __init__(self, token: str, db_user: User) -> None:
        self.token = token
        self.db_user = db_user

    @classmethod
    def from_token(cls, token: str | None, session: SessionDep) -> Self:
        if token is None:
            raise BusinessException.new(ErrorEnum.UNAUTHORIZED)
        user_id = redis_client.get(token)
        if user_id is None:
            raise BusinessException.new(ErrorEnum.UNAUTHORIZED)
        db_user: User | None = Dao(session, User).query_by_id(int(user_id))
        if db_user is None:
            raise BusinessException.new(ErrorEnum.UNAUTHORIZED)
        return cls(token, db_user)

    @classmethod
    def from_user(cls, user: User) -> Self:
        token = f"token_{snowflake_generator.generate_id()}"
        redis_client.set(token, user.model_dump_json(), settings.token_expire_seconds)
        return cls(token, user)

    def refresh(self):
        redis_client.set(self.token, self.db_user.model_dump_json(), ex_seconds=settings.token_expire_seconds)

    def logout(self) -> bool:
        redis_client.delete(self.token)
        return True

    @property
    def role(self) -> str:
        return self.db_user.role

    @property
    def user_id(self) -> int:
        return self.db_user.id
