#!/usr/bin/env bash

set -ex

echo "Installing Postgres 10"
sudo service postgresql stop
sudo apt-get remove -q 'postgresql-*'

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
RELEASE=$(lsb_release -cs)
echo "deb http://apt.postgresql.org/pub/repos/apt/ ${RELEASE}"-pgdg main | sudo tee  /etc/apt/sources.list.d/pgdg.list
sudo apt update -q
sudo apt install -q postgresql-11 postgresql-client-11
sudo cp /etc/postgresql/{9.6,11}/main/pg_hba.conf

echo "Restarting Postgres 10"
sudo service postgresql restart