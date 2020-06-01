# pull official base image
FROM python:3.8-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# check for updates
RUN apk update && apk upgrade

# install psycopg2 dependencies
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# install cffi dependencies
RUN apk add --no-cache openssl-dev libffi-dev

# install pillow dependencies
RUN apk add --no-cache jpeg-dev zlib-dev

# install pygraphviz dependencies
RUN apk add --no-cache graphviz graphviz-dev

# install brotli dependencies
RUN apk add --no-cache g++

# install uvicorn dependencies
RUN apk add --no-cache make

# install project dependencies
RUN pip install --upgrade setuptools
RUN pip install --upgrade virtualenv
RUN pip install poetry
COPY ./poetry.lock ./pyproject.toml /usr/src/app/

# Project initialization:
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# copy env_secrets_expand.sh
COPY ./env_secrets_expand.sh /usr/src/app/env_secrets_expand.sh

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# lint
RUN pip install flake8
COPY . /usr/src/app/
RUN flake8 --ignore=E501,F401 .

# run entrypoint.prod.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]