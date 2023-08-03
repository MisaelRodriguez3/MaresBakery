#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
pip insatll -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate