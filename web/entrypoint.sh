#!/bin/sh

. /usr/src/app/env_secrets_expand.sh
env_secrets_expand

if [ "$DATABASE" = "postgres" ]; then
  printf "\n\033[1mWaiting for postgres...\033[0m\n"
  while ! nc -z "$SQL_HOST_TEST" "$SQL_PORT_TEST"; do
    sleep 0.1
  done
  printf "PostgreSQL started\n\n"
fi

python manage.py collectstatic --no-input --clear
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata ./cookbook/fixtures/initial_data.json
python manage.py loaddata ./base/fixtures/initial_data.json

exec "$@"
