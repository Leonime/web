#!/bin/sh
if [ "$STAGE" = "development" ]; then
  . /usr/src/app/env_secrets_expand.sh
else
  . /home/app/web/env_secrets_expand.sh
fi

env_secrets_expand

if [ "$DATABASE" = "postgres" ]; then
  printf "\n\033[1mWaiting for postgres...\033[0m\n"
  while ! nc -z "$SQL_HOST_TEST" "$SQL_PORT_TEST"; do
    sleep 0.1
  done
  printf "PostgreSQL started\n\n"
fi

if [ "$CONTAINER" = "development" ]; then
  printf "#####\n"
  printf "# Django development setup\n"
  printf "#####\n"
  python manage.py collectstatic --no-input --clear
  python manage.py flush --no-input
  python manage.py makemigrations
  python manage.py migrate
  python manage.py loaddata ./cookbook/fixtures/initial_data.json
  python manage.py loaddata ./base/fixtures/initial_data.json
elif [ "$CONTAINER" = "production" ]; then
  printf "#####\n"
  printf "# Django production setup\n"
  printf "#####\n"
  python manage.py collectstatic --no-input --clear
  python manage.py migrate
  python manage.py loaddata ./cookbook/fixtures/initial_data.json
  python manage.py loaddata ./base/fixtures/initial_data.json
fi

exec "$@"
