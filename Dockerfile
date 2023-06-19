FROM python:3.10-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -e .

EXPOSE 80
