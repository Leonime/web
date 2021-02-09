# pull official base image
FROM python:3.9-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# needed to start installing dependencies
RUN apt-get update && apt-get -y upgrade

# install general required libraries
RUN apt-get -y install build-essential curl netcat

# install psycopg2 dependencies
RUN apt-get -y install libpq-dev

# install cffi dependencies
RUN apt-get -y install libffi-dev

# install pillow dependencies
RUN apt-get -y install libjpeg-dev zlib1g-dev

# install pygraphviz dependencies
RUN apt-get -y install graphviz graphviz-dev

# install npm
RUN curl -sL https://deb.nodesource.com/setup_15.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g npm@next

# install project dependencies
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
RUN flake8 --ignore=E501,F401,F403 .

# react
WORKDIR /usr/src/app/frontend
RUN npm install
RUN npm audit fix --force
RUN npm run dev
RUN npx browserslist@latest --update-db
WORKDIR /usr/src/app/

# run entrypoint.prod.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]