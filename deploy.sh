#!/bin/bash
set -e  # stop on any error

echo "── Pulling latest code ──"
git pull origin main

echo "── Activating virtualenv ──"
source venv/bin/activate

echo "── Installing dependencies ──"
pip install -r requirements.txt --quiet

echo "── Collecting static files ──"
python manage.py collectstatic --noinput

echo "── Running migrations ──"
python manage.py migrate --run-syncdb

echo "── Restarting service ──"
systemctl restart starikolasin

echo "✓ Deploy complete"
