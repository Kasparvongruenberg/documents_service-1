# Documents Service
Microservice for the documents API

## Deploy locally via Docker

Build first the images:

```bash
docker-compose -f docker-compose-dev.yml build # --no-cache to force deps installation
```

To run the webserver (go to 127.0.0.1:8080):

```bash
docker-compose -f docker-compose-dev.yml up # -d for detached
```

User: `admin`
Password: `admin`.

To run the tests:

```bash
docker-compose -f docker-compose-dev.yml run --entrypoint '/usr/bin/env' --rm documents_service python manage.py test # --keepdb to run second time faster
```

## Deploy to server