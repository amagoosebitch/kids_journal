from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    telegram_token: str
    telegram_login: str

    class Config:
        env_prefix = "AUTH_"


def load_bot_config():
    return BotConfig()
