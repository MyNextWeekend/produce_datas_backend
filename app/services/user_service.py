from typing import Self

from app.core.dependencies import SessionDep
from app.core.exception import BusinessException, ErrorEnum
from app.dao import Dao
from app.models.first_model import User
from app.utils.redis_utils import RedisClient
from app.utils.snow_utils import snowflake_generator


class UserService:
    TOKEN_EXPIRE_SECONDS = 60 * 60  # 1h
    _redis = RedisClient()

    def __init__(self, token: str, db_user: User) -> None:
        self.token = token
        self.db_user = db_user

    @classmethod
    def from_token(cls, token: str | None, session: SessionDep) -> Self:
        if token is None:
            raise BusinessException.new(ErrorEnum.UNAUTHORIZED)
        user_id = cls._redis.get(token)
        if user_id is None:
            raise BusinessException.new(ErrorEnum.UNAUTHORIZED)
        db_user: User | None = Dao(session, User).query_by_id(int(user_id))
        if db_user is None:
            raise BusinessException.new(ErrorEnum.UNAUTHORIZED)
        return cls(token, db_user)

    @classmethod
    def login(cls, user: User) -> str:
        token = f"token_{snowflake_generator.generate_id()}"
        cls._redis.set(token, user.model_dump_json(), cls.TOKEN_EXPIRE_SECONDS)
        return token

    def refresh(self):
        self._redis.set(self.token, "", ex_seconds=self.TOKEN_EXPIRE_SECONDS)

    def logout(self):
        self._redis.delete(self.token)

    @property
    def role(self) -> str:
        return self.db_user.role

    @property
    def user_id(self) -> int:
        return self.db_user.id
