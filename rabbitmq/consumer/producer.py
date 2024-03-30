import asyncio
import aio_pika

async def produce(queue_name, message_body):
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()

    await channel.declare_queue(queue_name, auto_delete=True)

    await channel.default_exchange.publish(
        aio_pika.Message(body=message_body.encode()),
        routing_key=queue_name
    )

    print("Message sent:", message_body)


async def main():
    queue_name = "email_queue"
    message = "Hello, RabbitMQ!"
    await produce(queue_name, message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
