from contextlib import asynccontextmanager

import uvicorn

import broker

from api.v1 import content

from broker.producer import RabbitMQ

from core.config import config
from fastapi import FastAPI

dependencies = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbit = RabbitMQ("amqp://guest:guest@localhost/")
    await rabbit.connect_broker()
    broker.producer.rabbit_producer = rabbit
    yield
    await rabbit.close()


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    dependencies=dependencies,
    lifespan=lifespan,
)

app.include_router(content.router, prefix='/api/v1/user_event', tags=['USER_EVENT'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
