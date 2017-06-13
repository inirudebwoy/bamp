FROM python:2-alpine

RUN apk update
RUN apk add gcc
RUN apk add musl-dev

RUN pip install --upgrade virtualenv tox && \
        virtualenv --always-copy /ve

COPY . /src/bamp
WORKDIR /src/bamp
RUN /ve/bin/pip install -r requirements-dev.pip