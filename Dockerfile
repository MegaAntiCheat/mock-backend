FROM python:3.10-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -e .

RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    postgresql-client

ENV DATABASE_URL=postgresql://postgres:@db:5432/demos
EXPOSE 80
