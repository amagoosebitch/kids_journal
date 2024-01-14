from pydantic_settings import BaseSettings


class JWTSettings(BaseSettings):
    algorithm: str = "HS256"
    secret_key: str

    class Config:
        env_prefix = "JWT_"
