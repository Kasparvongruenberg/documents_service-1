#!/bin/bash
# This script must not be used for production. Migrating, collecting static
# data, check database connection should be done by different jobs in
# at a different layer.

set -e

bash tcp-port-wait.sh $DATABASE_HOST $DATABASE_PORT

echo "Migrate"
python manage.py migrate

if [ "$nginx" == "true" ]; then
    echo "Collect static"
    python manage.py collectstatic --no-input
fi

echo "Creating admin user"
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(email='admin@humanitec.com').delete(); User.objects.create_superuser('admin', 'admin@humanitec.com', 'admin')"

echo "Running the server"
PYTHONUNBUFFERED=1 python manage.py runserver 0.0.0.0:8081
