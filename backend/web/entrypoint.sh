#!/bin/sh
set -e

echo "Waiting for MariaDB..."
until python -c "
import MySQLdb, os
MySQLdb.connect(
    host=os.environ['DB_HOST'],
    port=int(os.environ.get('DB_PORT', 3306)),
    user=os.environ['DB_USER'],
    passwd=os.environ['DB_PASSWORD'],
    db=os.environ['DB_NAME'],
)
" 2>/dev/null; do
  sleep 1
done

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn web.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 120
