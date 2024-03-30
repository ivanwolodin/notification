import logging
import json
from abc import abstractmethod, ABC
from typing import Optional

import aio_pika
# import backoff as backoff
from aio_pika import connect, Message

from core.config import config


class BaseProducer(ABC):
    @abstractmethod
    async def connect_broker(self, *args, **kwargs):
        pass

    @abstractmethod
    async def produce(self, *args, **kwargs):
        pass

    async def close(self, *args, **kwargs):
        pass


class RabbitMQ(BaseProducer):

    def __init__(self, dsn):
        self.dsn = dsn
        self.connection = None
        self.queue = None

    async def connect_broker(self):
        self.connection = await connect(self.dsn)
        return self.connection

    async def close(self):
        try:
            await self.connection.close()
        except Exception as e:
            raise e

    async def create_queue(self):
        async with self.connection.channel() as channel:
            self.queue = await channel.declare_queue(
                config.RABBIT_Q_NAME,
                durable=True,
            )

    async def produce(self, message) -> bool:
        # connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
        if not self.queue:
            await self.create_queue()

        async with self.connection.channel() as channel:
            # channel = await self.connection.channel()

            exchange = await channel.declare_exchange('users', aio_pika.ExchangeType.DIRECT)
            queue = await channel.declare_queue(self.queue.name, durable=True)

            await queue.bind(exchange, self.queue.name)

            pika_message = aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            )

            await exchange.publish(pika_message, routing_key=self.queue.name)
            return True


rabbit_producer: Optional[RabbitMQ] = None


def get_rabbit_producer():
    return rabbit_producer
