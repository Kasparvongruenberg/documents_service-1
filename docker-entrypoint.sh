#!/bin/bash

echo $(date -u) " - Migrating"
python manage.py migrate

echo $(date -u) "- Collect Static"
python manage.py collectstatic --no-input

echo $(date -u) "- Creating admin user"
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

echo $(date -u) "- Running the server"
gunicorn -b 0.0.0.0:8080 --reload -w 2 --timeout 120 document_service.wsgi
