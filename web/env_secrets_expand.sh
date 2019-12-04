#!/bin/sh

: "${ENV_SECRETS_DIR:=/run/secrets}"

env_secret_debug()
{
  if [ "$ENV_SECRETS_DEBUG" = true ]; then
    printf "\033[1m%s\033[0m\n" "$*"
  fi
}

# usage: env_secret_expand VAR
#    ie: env_secret_expand 'XYZ_DB_PASSWORD'
# (will check for "$XYZ_DB_PASSWORD" variable value for a placeholder that defines the
#  name of the docker secret to use instead of the original value. For example:
# XYZ_DB_PASSWORD={{DOCKER-SECRET:my-db.secret}}
env_secret_expand() {
  var="$1"
  eval val=\$"$var"
  if secret_name=$(expr match "$val" "{{DOCKER_SECRET:\([^}]\+\)}}$"); then
    secret="${ENV_SECRETS_DIR}/${secret_name}"
    env_secret_debug "Secret file for $var: $secret"
    if [ -f "$secret" ]; then
      val=$(cat "${secret}")
      export "$var"="$val"
      env_secret_debug "Expanded variable: $var=$val"
    else
      env_secret_debug "Secret file does not exist! $secret"
    fi
  fi
}

env_secrets_expand() {
  for env_var in $(printenv | cut -f1 -d"=")
  do
    env_secret_expand "$env_var"
  done

  if [ "$ENV_SECRETS_DEBUG" = true ]; then
    printf "\n\033[1mEnvironment variables\033[0m\n"
    printenv
  fi
}
