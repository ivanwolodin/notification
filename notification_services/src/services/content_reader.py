from notification_services.src.broker.producer import RabbitMQ
from notification_services.src.core.config import config
from notification_services.src.core.sql import SQL_QUERIES
from notification_services.src.db.db_connection import open_postgres_connection


class NotifyBroker:

    def __init__(self):
        self.sql_queries = SQL_QUERIES
        self.notify_list = []

    def db_read(self):
        with open_postgres_connection() as pg_cursor:
            pg_cursor.execute(
                self.sql_queries.get("EVERY_X_DAYS")
            )
            self.notify_list = [notify for notify in pg_cursor.fetchall()]
            return True

    async def notify_broker(self):
        rabbit = RabbitMQ(config.RABBIT_DSN)
        await rabbit.connect_broker()
        with open_postgres_connection() as pg_cursor:
            for note in self.notify_list:
                produce_access = await rabbit.produce({note[0]: note[1]})
                if produce_access:
                    pg_cursor.execute(
                        self.sql_queries.get("PROCESSED_ROWS"),
                        (note[0]),
                    )
