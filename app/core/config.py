from pathlib import Path, PosixPath
from typing import Optional

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class MysqlSettings(BaseSettings):
    # 数据库配置
    host: str
    port: int
    user: str
    password: str
    database: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def uri(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="mysql+pymysql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.database,
        )


class RedisSettings(BaseSettings):
    # redis配置
    host: str
    port: int
    password: Optional[str] = None

    @computed_field
    @property
    def uri(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/0"
        return f"redis://{self.host}:{self.port}/0"


class SqliteSettings(BaseSettings):
    path: str


class LogSettings(BaseSettings):
    path: str
    file: str


class Settings(BaseSettings):
    # 项目的根目录
    root_dir: PosixPath = Path(__file__).resolve().parent.parent.parent
    local_repository: PosixPath = root_dir / 'local_repository'

    mysql: MysqlSettings
    sqlite: SqliteSettings
    redis: RedisSettings
    log: LogSettings

    model_config = SettingsConfigDict(
        # 配置文件位置，项目根目录 .env 文件
        env_file=root_dir.joinpath('.env'),
        env_ignore_empty=True,
        extra="ignore",
        env_nested_delimiter="__"
    )

    # 日志文件位置
    # log_file: str = os.path.join(root_dir, "logs", "system.log")
    @computed_field
    @property
    def log_file(self) -> str:
        log_path = self.root_dir.joinpath(self.log.path)
        if not log_path.is_dir():
            log_path.mkdir(exist_ok=True)
        return str(log_path.joinpath(self.log.file))

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sqlite_uri(self) -> str:
        return f"sqlite:///{self.root_dir}/{self.sqlite.path}"


settings = Settings()
