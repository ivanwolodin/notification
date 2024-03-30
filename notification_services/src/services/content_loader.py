from functools import lru_cache

from broker.producer import RabbitMQ, BaseProducer, get_rabbit_producer
from fastapi import Depends
from models.content_model import BaseContent


class ContentService:

    def __init__(self, producer: BaseProducer):
        self.producer: BaseProducer = producer

    async def produce(self, data: BaseContent) -> None:
        await self.producer.produce({data.user_id: data.event_type})


@lru_cache()
def get_content_loader_service(producer: RabbitMQ = Depends(get_rabbit_producer)) -> ContentService:
    return ContentService(producer)
