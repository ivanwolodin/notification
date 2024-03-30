from pydantic import Field
from pydantic_settings import BaseSettings



class Config(BaseSettings):
    PROJECT_NAME: str = Field("User events", env="PROJECT_NAME")
    BACKOFF_MAX_TRIES: int = Field(100, env="BACKOFF_MAX_TRIES")
    RABBIT_Q_NAME: str = Field("NOTIFY_1", env="RABBIT_TOPIC_NAME")
    RABBIT_DSN: str = Field("kafka:29099", env="RABBIT_DSN")
    # CLICK_HOST: str = Field("clickhouse-node1", env="CLICK_HOST")
    # CLICK_PORT: str = Field("9000", env="CLICK_PORT")
    # ETL_SLEEP_SECOND: int = Field(5, env="ETL_SLEEP_SECOND")
    # ETL_BATCH_MESSAGE_COUNT: int = Field(1, env="ETL_BATCH_MESSAGE_COUNT")
    # TABLE_NAME: str = Field("table_ugc", env="TABLE_NAME")
    # DB_NAME: str = Field("ugc", env="DB_NAME")


config = Config()

