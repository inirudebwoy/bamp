FROM python:2

RUN apt-get update
RUN pip install --upgrade virtualenv tox && \
        virtualenv --always-copy /ve

COPY . /src/bamp
WORKDIR /src/bamp
RUN /ve/bin/pip install -r requirements-dev.pip