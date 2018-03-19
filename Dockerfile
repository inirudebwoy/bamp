FROM python:2

COPY . /src/bamp
WORKDIR /src/bamp
RUN pip install -r requirements-dev.pip
