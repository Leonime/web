#!/bin/sh
if [ "$STAGE" = "development" ]; then
  . /usr/src/app/env_secrets_expand.sh
else
  . /home/app/web/env_secrets_expand.sh
fi

env_secrets_expand

if [ "$DATABASE" = "postgres" ]; then
  printf "#################################\n"
  printf "# \033[1mWaiting for postgres...\033[0m#\n"
  printf "#################################\n\n"
  while ! nc -z "$SQL_HOST_TEST" "$SQL_PORT_TEST"; do
    sleep 0.1
  done
  printf "######################\n"
  printf "# PostgreSQL started #\n"
  printf "######################\n\n"
fi

if [ "$CONTAINER" = "development" ]; then
  printf "############################\n"
  printf "# Django development setup #\n"
  printf "############################\n\n"
  python manage.py collectstatic --no-input --clear -v 0
  python manage.py makemigrations
  python manage.py migrate
  CONTAINER_FIRST_RUN="/var/lib/codeshepherds/data/CONTAINER_HAS_RUN_BEFORE"
  if [ ! -e $CONTAINER_FIRST_RUN ]; then
    touch $CONTAINER_FIRST_RUN
    printf "###########################\n"
    printf "# First container startup #\n"
    printf "###########################\n\n"
    # LOGIC HERE
    python manage.py loaddata ./cookbook/fixtures/initial_data.json
    python manage.py loaddata ./base/fixtures/initial_data.json
  else
    printf "###############################\n"
    printf "# Not first container startup #\n"
    printf "###############################\n\n"
  fi
elif [ "$CONTAINER" = "production" ]; then
  printf "#########################\n"
  printf "# Django production setup\n"
  printf "#########################\n\n"
  python manage.py collectstatic --no-input --clear -v 0
  python manage.py migrate
  CONTAINER_FIRST_RUN="/var/lib/codeshepherds/data/CONTAINER_HAS_RUN_BEFORE"
  if [ ! -e $CONTAINER_FIRST_RUN ]; then
    touch $CONTAINER_FIRST_RUN
    printf "###########################\n"
    printf "# First container startup #\n"
    printf "###########################\n\n"
    # LOGIC HERE
    python manage.py loaddata ./cookbook/fixtures/initial_data.json
    python manage.py loaddata ./base/fixtures/initial_data.json
  else
    printf "###############################\n"
    printf "# Not first container startup #\n"
    printf "###############################\n\n"
  fi
fi

SIMPLE_HISTORY_FIRST_RUN="/var/lib/codeshepherds/data/SIMPLE_HISTORY_FIRST_RUN"

if [ ! -e $SIMPLE_HISTORY_FIRST_RUN ]; then
  printf "############################\n"
  printf "# Simple history first run #\n"
  printf "############################\n\n"
  touch $SIMPLE_HISTORY_FIRST_RUN
  python manage.py populate_history --auto
else
  printf "###############################\n"
  printf "# Simple history has been run #\n"
  printf "###############################\n\n"
fi

exec "$@"
