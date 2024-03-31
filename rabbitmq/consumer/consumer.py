import asyncio
import os

import aio_pika

from email_sender_async import send_email


async def consume(queue_name):
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbit_queue/")
    channel = await connection.channel()
    queue = await channel.declare_queue(
        queue_name,
        auto_delete=True,
    )

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:

            async with message.process() as msg:
                get_from_rabbit = msg.body.decode()
                await send_email(
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
