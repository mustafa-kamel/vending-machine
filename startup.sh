#!/usr/bin/env sh

python /opt/vending-machine/manage.py collectstatic --no-input
python /opt/vending-machine/manage.py migrate

hypercorn -b 0.0.0.0:${PORT} asgi:application
