# pull official base image
FROM python:3.7-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# install cffi dependencies
RUN apk add --no-cache openssl-dev libffi-dev

# install pillow dependencies
RUN apk add --no-cache jpeg-dev zlib-dev

# install pygraphviz dependencies
RUN apk add --no-cache graphviz graphviz-dev

# install project dependencies
RUN pip install pipenv
COPY ./Pipfile* /usr/src/app/
RUN pipenv lock -r > requirements.txt
# Pipenv insist on creating a virtualenv lets delete it.
RUN pipenv --rm
# It's recommended to use pip to install dependancies on docker containers.
RUN pip install -v --no-cache-dir -r requirements.txt

# copy env_secrets_expand.sh
COPY ./env_secrets_expand.sh /usr/src/app/env_secrets_expand.sh

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.prod.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]