FROM python:3.11
WORKDIR /app

COPY requirements.txt abstract_sender.py  __init__.py email_sender_async.py settings.py /app/

RUN pip install -r requirements.txt

COPY consumer.py /app/

CMD ["python", "consumer.py"]