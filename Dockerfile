FROM python:3.7-alpine 
# 
LABEL Mcuve WorkOutTracker

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client 
# install the apk for the postgres client witout unessesary cache
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
#  this are temporarly requirements for installing postgresql

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /app

WORKDIR /app

COPY ./app /app

RUN adduser -D user
# create a user for running our process

USER user
# switch to the user