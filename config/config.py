import os
import logging
from typing import Literal
from dataclasses import dataclass

from pydantic import SecretStr, PostgresDsn
from environs import Env

logger = logging.Logger(__name__)


@dataclass
class BotSettings:
    token: SecretStr
    assets_chat_id: int
    club_chat_id: int
    admin_id: int


@dataclass
class DBSettings:
    dsn: PostgresDsn


@dataclass
class RedisSettings:
    host: str
    port: int
    db: int
    username: str
    password: SecretStr


@dataclass
class LogSettings:
    level: str
    format: str
    style: Literal["%", "{", "$"]


@dataclass
class YooSettings:
    token: SecretStr


@dataclass
class Config:
    bot: BotSettings
    db: DBSettings
    redis: RedisSettings
    log: LogSettings
    yoo: YooSettings


def load_config(path: str | None = None) -> Config:
    "Loads configuration for the app."
    env = Env()
    _is_docker = env.bool("RUNNING_IN_DOCKER", False)

    if not _is_docker:
        if path:
            if not os.path.exists(path):
                logger.warning(f".env file was not fount in the '{path}'")
            else:
                logger.info(f"Loading .env file from '{path}'...")

        env.read_env(path)

    token = SecretStr(env("BOT_TOKEN"))
    if not token:
        raise ValueError("BOT_TOKEN must not be empty")

    bot = BotSettings(
        token=token,
        assets_chat_id=env.int("ASSETS_CHAT_ID"),
        club_chat_id=env.int("CLUB_CHAT_ID"),
        admin_id=env.int("ADMIN_ID"),
    )

    db_name = env("POSTGRES_DB")
    db_host = env("POSTGRES_HOST") if _is_docker else "localhost"
    db_port = env.int("POSTGRES_PORT")
    db_username = env("POSTGRES_USER")
    db_password = SecretStr(env("POSTGRES_PASSWORD"))
    db = DBSettings(
        dsn=f"postgresql+asyncpg://{db_username}:{db_password.get_secret_value()}@{db_host}:{db_port}/{db_name}"
    )

    redis = RedisSettings(
        host=env("REDIS_HOST") if _is_docker else "localhost",
        port=env.int("REDIS_PORT"),
        db=env.int("REDIS_DATABASE"),
        password=SecretStr(env("REDIS_PASSWORD")),
        username=env("REDIS_USERNAME"),
    )

    log = LogSettings(
        level=env("LOG_LEVEL"), format=env("LOG_FORMAT"), style=env("LOG_STYLE")
    )

    yoo = YooSettings(token=SecretStr(env("YOO_TOKEN")))

    logger.info("Configuration loaded successfully")
    return Config(
        bot=bot,
        db=db,
        redis=redis,
        log=log,
        yoo=yoo,
    )
