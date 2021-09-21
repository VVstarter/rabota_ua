# syntax=docker/dockerfile:1
FROM python:3-slim
RUN apt-get update
RUN pip install --upgrade pip
RUN mkdir rabota_ua_requests
WORKDIR /rabota_ua_requests
COPY . /rabota_ua_requests
RUN pip install -r requirements.txt
CMD python runner.py