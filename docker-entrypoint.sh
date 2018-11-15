#!/bin/bash

echo $(date -u) " - Migrating"
python manage.py migrate

echo $(date -u) "- Collect Static"
python manage.py collectstatic --no-input

RESULT=$?
if [ $RESULT -ne 0 ]; then
    echo $(date -u) " - There was a problem migrating. Setting up the maintenance page"
    pushd templates/maintenance/; python -m SimpleHTTPServer 8081; popd
else
    echo $(date -u) " - Running the server in branch '$branch'"

    if [ "$branch" == "dev" ]; then
        gunicorn -b 0.0.0.0:8080 documents-service.wsgi --reload
    else
        gunicorn -b 0.0.0.0:8080 documents-service.wsgi
    fi
fi
