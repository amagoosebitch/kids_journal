from pydantic.env_settings import BaseSettings


class YDBSettings(BaseSettings):
    endpoint: str = "grpc://localhost:2136"
    database: str = "/local"

    class Config:
        env_prefix = "YDB_"
