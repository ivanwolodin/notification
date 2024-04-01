from contextlib import asynccontextmanager

import uvicorn
from api.v1 import content
from broker import producer
from broker.producer import RabbitMQ
from core.config import config
from fastapi import FastAPI
from services.scheduler import Scheduler

dependencies = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = Scheduler()
    scheduler.start_scheduler()
    rabbit = RabbitMQ(config.RABBIT_DSN)
    await rabbit.connect_broker()
    producer.rabbit_producer = rabbit
    yield
    await rabbit.close()
    scheduler.stop_scheduler()


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    dependencies=dependencies,
    lifespan=lifespan,
)

app.include_router(
    content.router, prefix='/api/v1/user_event', tags=['USER_EVENT']
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
