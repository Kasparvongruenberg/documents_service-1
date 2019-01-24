# Documents Service

Microservice for the documents API. It allows the user to store static files
in Amazon S3.

## Deploy locally via Docker

Build first the images:

```bash
docker-compose build # --no-cache to force deps installation
```

To run the webserver (go to 127.0.0.1:8004):

```bash
docker-compose up # -d for detached
```

User: `admin`
Password: `admin`.

To run the tests only once:

```bash
docker-compose run --entrypoint 'bash scripts/run-tests.sh' --rm documents_service
```

To run the tests and open the bash when they are finished - useful to allow
you work faster if you want to run them more than once:

```bash
docker-compose run --entrypoint 'bash scripts/run-tests.sh --bash-on-finish' --rm documents_service
```

To run bash:

```bash
docker-compose run --entrypoint 'bash' --rm documents_service
```

## Deploy to server

### Environment Variables

The following environment variables need to be configured in  order to make 
the service work correctly:
* `ALLOWED_HOSTS`
* `CORS_ORIGIN_WHITELIST`
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