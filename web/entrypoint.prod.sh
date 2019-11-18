#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  printf "\n\033[1mWaiting for postgres...\033[0m\n"
  while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
    sleep 0.1
  done
  printf "PostgreSQL started\n\n"
fi

exec "$@"
