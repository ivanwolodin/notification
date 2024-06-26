from functools import lru_cache

from broker.producer import BaseProducer, RabbitMQ, get_rabbit_producer
from fastapi import Depends
from models.content_model import BaseContent


class ContentService:
    def __init__(self, producer: BaseProducer):
        self.producer: BaseProducer = producer

    async def produce(self, data: BaseContent) -> None:
        data.user_id = await self.get_email_from_auth_service(data.user_id)
        await self.producer.produce(
            {
                'email_list': [data.user_id],
                'event_type': data.event_type,
                'subject': data.subject,
                'text': data.body,
            }
        )

    @staticmethod
    async def get_email_from_auth_service(user_id: str) -> str:
        """Get email from auth service by user_id"""
        return 'example@example.com'


@lru_cache()
def get_content_loader_service(
    producer: RabbitMQ = Depends(get_rabbit_producer),
) -> ContentService:
    return ContentService(producer)
