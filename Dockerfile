FROM python:3.7-alpine 
# 
LABEL Mcuve WorkOutTracker

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /app

WORKDIR /app

COPY ./app /app

RUN adduser -D user
# create a user for running our process

USER user
# switch to the user