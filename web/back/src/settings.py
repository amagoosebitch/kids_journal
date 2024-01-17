from functools import cache

from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    telegram_token: str
    telegram_login: str

    class Config:
        env_prefix = "AUTH_"


class APIServerSettings(BaseSettings):
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]

    class Config:
        env_prefix = "API_SERVER_"


@cache
def load_bot_config() -> BotConfig:
    return BotConfig()


@cache
def load_api_settings() -> APIServerSettings:
    return APIServerSettings()
