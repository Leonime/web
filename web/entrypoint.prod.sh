#!/bin/sh

. /home/app/web/env_secrets_expand.sh
env_secrets_expand

if [ "$DATABASE" = "postgres" ]
then
  printf "\n\033[1mWaiting for postgres...\033[0m\n"
  while ! nc -z "$SQL_HOST_TEST" "$SQL_PORT_TEST"; do
    sleep 0.1
  done
  printf "PostgreSQL started\n\n"
fi

exec "$@"
