#!/bin/bash

python3 -m pip install --user virtualenv
python3 -m venv new_pyenv
. ./new_pyenv/bin/activate
pip3 install PyQt5
pip3 install Pillow
pip3 install imageio
pip3 install matplotlib
pip3 install psycopg2
pip3 install opencv-python
pip3 install numpy
. deactivate