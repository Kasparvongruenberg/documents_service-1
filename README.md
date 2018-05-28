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

### Environment Variables
The following environment variables need to be configured in  order to make 
the service work correctly:
* `DATABASE_ENGINE` 
* `DATABASE_NAME` 
* `DATABASE_USER` 
* `DATABASE_PASSWORD` 
* `DATABASE_PORT` and `DATABASE_HOST` are optional
 
 If AWS S3 Buckets should be used for storing documents the following 
 settings are required as well:
 * `AWS_ACCESS_KEY_ID`
 * `AWS_ACCESS_KEY_SECRET`
 * `AWS_S3_BUCKET`