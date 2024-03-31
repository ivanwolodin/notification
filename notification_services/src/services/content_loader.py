from functools import lru_cache

from fastapi import Depends

from broker.producer import BaseProducer, RabbitMQ, get_rabbit_producer
from models.content_model import BaseContent


class ContentService:

    def __init__(self, producer: BaseProducer):
        self.producer: BaseProducer = producer

    async def produce(self, data: BaseContent) -> None:
        await self.producer.produce({
            'user_id': [data.user_id],
            'event_type': data.event_type,
            'subject': data.subject,
            'text': data.body,
        })


@lru_cache()
def get_content_loader_service(producer: RabbitMQ = Depends(get_rabbit_producer)) -> ContentService:
    return ContentService(producer)
