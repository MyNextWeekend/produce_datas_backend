from app.models.first_model import User
from app.utils.redis_utils import RedisClient


class UserService:
    def __init__(self, db_user: User, token: str) -> None:
        self.token = token
        self.db_user = db_user

    def refresh(self):
        client = RedisClient()
        client.set(self.token, "", ex_seconds=60 * 60)

    def logout(self):
        client = RedisClient()
        client.delete(self.token)

    def get_role(self):
        return self.db_user.role
