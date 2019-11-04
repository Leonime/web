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

# install dependencies
RUN pip install pipenv
COPY ./Pipfile* /usr/src/app/
RUN pipenv install --ignore-pipfile --system --dev -v

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
