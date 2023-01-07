# dockerfile base on python image
FROM python:3.8-slim

WORKDIR /worker

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ADD . /worker

# ENTRYPOINT celery --app tasks worker --loglevel=INFO