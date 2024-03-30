import asyncio
import aio_pika

from email_sender import email_send

async def consume(queue_name):
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbit_queue/")

    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name, auto_delete=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:

            async with message.process() as msg:
                email_send()
                # await send_mail_async(
                #     sender='volodin.v-i-v@yandex.ru',
                #     to=['volodin.v-i-v@yandex.ru'],
                #     subject='sdfsdf',
                #     text='sdf',
                # )
                print("Received message:", msg.body.decode())


async def main():
    queue_name = "email_queue"
    await consume(queue_name)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

