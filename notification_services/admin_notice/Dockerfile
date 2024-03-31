FROM python:3.10

WORKDIR /code

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
RUN ["chmod", "+x", "run_uwsgi.sh"]

ENTRYPOINT ["./run_uwsgi.sh"]

# RUN chmod a+x ./scripts/run_celery.sh