# syntax=docker/dockerfile:1
FROM python:3-slim
RUN apt-get update
RUN pip install --upgrade pip
RUN mkdir rabota_ua_scrapy
WORKDIR /rabota_ua_scrapy
COPY . /rabota_ua_scrapy
RUN pip install -r requirements.txt
CMD python main.py