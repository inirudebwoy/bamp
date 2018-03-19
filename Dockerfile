FROM python:2

COPY . /src/bamp
WORKDIR /src/bamp
RUN /ve/bin/pip install -r requirements-dev.pip
