FROM python:2

WORKDIR /ve
COPY . /ve/bamp

RUN apt-get update
RUN pip install --upgrade virtualenv tox && \
        virtualenv --always-copy /ve
RUN /ve/bin/pip install -r bamp/requirements-dev.pip