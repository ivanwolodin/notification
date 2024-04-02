import os


class Settings:

    RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER', 'guest')
    RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS', 'guest')
    RABBITMQ_CONTAINER_NAME = os.getenv(
        'RABBITMQ_CONTAINER_NAME', 'rabbit_queue'
    )
    RABBITMQ_QUEUE_NAME = os.getenv('RABBITMQ_QUEUE_NAME', 'email_queue')

    SMTP_USER = (os.getenv('SMTP_USER'),)


settings = Settings()
