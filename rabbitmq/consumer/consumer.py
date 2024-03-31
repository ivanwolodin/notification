import asyncio
import os

import aio_pika

from email_sender_async import email_sender


async def consume(queue_name):
    connection = await (
        aio_pika.connect_robust(
            f"amqp://{os.getenv('RABBITMQ_DEFAULT_USER')}"
            f":{os.getenv('RABBITMQ_DEFAULT_PASS')}@"
            f"{os.getenv('RABBITMQ_CONTAINER_NAME')}/"
        )
    )

    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name, auto_delete=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:

            async with message.process() as msg:
                get_from_rabbit = msg.body.decode()
                await email_sender.send_mail(
                    sender=os.getenv('SMTP_USER'),
                    to=get_from_rabbit.get('email_list'),
                    subject=get_from_rabbit.get('subject'),
                    text=get_from_rabbit.get('text'),
                )


async def main():
    queue_name = 'email_queue'
    await consume(queue_name)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
