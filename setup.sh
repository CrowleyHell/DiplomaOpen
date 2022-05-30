#!/bin/bash

python3 -m pip install --user virtualenv
python3 -m venv new_pyenv
. ./new_pyenv/bin/activate
apt-get install -y \
        python3 \
        pyqt5-dev python3-pyqt5 \
        python3-psycopg2

apt-get install -y python3-opencv
pip3 install Pillow
pip3 install imageio
pip3 install matplotlib
pip3 install numpy
. deactivate