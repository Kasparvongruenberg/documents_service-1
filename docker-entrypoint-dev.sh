#!/bin/bash

bash scripts/tcp-port-wait.sh $DATABASE_HOST $DATABASE_PORT

echo $(date -u) "- Migrating"
python manage.py migrate

echo $(date -u) "- Creating admin user"
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

echo $(date -u) "- Collect Static"
python manage.py collectstatic --no-input

echo $(date -u) "- Running the server"
gunicorn -b 0.0.0.0:8080 documents-service.wsgi -w 2 \
 --timeout 120 --reload --log-level debug