FROM python:3.11

WORKDIR /

COPY requirements.txt .

RUN apt-get update && \
    pip install -r requirements.txt --no-cache-dir

COPY .. .

CMD ["python", "./main.py"]
