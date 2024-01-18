from functools import cache

from pydantic_settings import BaseSettings


class JWTSettings(BaseSettings):
    algorithm: str = "HS256"
    secret_key: str

    class Config:
        env_prefix = "JWT_"


@cache
def create_jwt_settings() -> JWTSettings:
    return JWTSettings()


class RedirectSettings(BaseSettings):
    main_url: str = "https://d5daf6rq7hsttsotir3o.apigw.yandexcloud.net"
    login: str = "https://d5daf6rq7hsttsotir3o.apigw.yandexcloud.net/login"

    class Config:
        env_prefix = "REDIRECT_"


@cache
def create_redirect_settings() -> RedirectSettings:
    return RedirectSettings()

