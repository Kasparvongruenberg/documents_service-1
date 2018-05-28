FROM python:3.6

COPY . /code
WORKDIR /code

RUN pip install -r requirements/production.txt

EXPOSE 8081

ARG BRANCH=None
ENV branch=${BRANCH}

ENTRYPOINT ["/code/docker-entrypoint.sh"]
