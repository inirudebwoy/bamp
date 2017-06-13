FROM python:3.6-alpine

RUN apk update
RUN apk add python
RUN apk add python3