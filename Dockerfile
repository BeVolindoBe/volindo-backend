FROM python:alpine3.15

RUN apk update && apk upgrade

WORKDIR /code
COPY . /code/

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
