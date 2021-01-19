FROM python:3.9-slim-buster

RUN apt-get -y update && apt-get -y upgrade

RUN apt-get install -y git

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app
