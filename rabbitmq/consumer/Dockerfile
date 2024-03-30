FROM python:3.11
WORKDIR /app

COPY requirements.txt /app/
COPY __init__.py /app/
COPY email_sender_async.py /app/
COPY email_sender.py /app/

RUN pip install -r requirements.txt

COPY consumer.py /app/consumer.py

CMD ["python", "consumer.py"]
