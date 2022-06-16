#!/bin/bash

add-apt-repository universe -enter
apt-get update
apt-get install python3-pip
apt install python3.9-venv
python3 -m pip install --user virtualenv
python3 -m venv new_pyenv
. ./new_pyenv/bin/activate
apt-get install -y \
python3 \
pyqt5-dev python3-pyqt5 \
python3-pyqt5 \
python3-psycopg2

apt-get install -y python3-opencv
apt-get install postgresql
apt-get install postgresql postgresql-client
apt-get install postgresql postgresql-contrib
apt-get install postgresql-client
pip3 install Pillow
pip3 install imageio
pip3 install matplotlib
pip3 install numpy
systemctl status postgresql --no-pager
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'devint56';"
PGPASSWORD=devint56 psql -h localhost -d postgres -U postgres -f base.sql
deactivate