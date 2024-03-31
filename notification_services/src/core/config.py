from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    PROJECT_NAME: str = Field("User events", env="PROJECT_NAME")
    BACKOFF_MAX_TRIES: int = Field(100, env="BACKOFF_MAX_TRIES")
    RABBIT_Q_NAME: str = Field("NOTIFY_1", env="RABBIT_TOPIC_NAME")
    RABBIT_DSN: str = Field("amqp://guest:guest@rabbitmq/", env="RABBIT_DSN")
    RABBIT_EXCHANGE: str = Field("users", env="users")
    SCHEDULER_INTERVAL: int = Field(1, env="SCHEDULER_INTERVAL")
    PG_DB: str = Field("notify", env="PG_DB")
    PG_HOST: str = Field("postgres", env="PG_HOST")
    PG_PORT: str = Field("5432", env="PG_PORT")
    PG_USER: str = Field("admin", env="PG_USER")
    PG_PASSWORD: str = Field("password", env="PG_PASSWORD")


config = Config()
