FROM python:3.6

WORKDIR /code

COPY ./requirements/base.txt requirements/base.txt
COPY ./requirements/production.txt requirements/production.txt
RUN pip install -r requirements/production.txt

ADD . /code

EXPOSE 8080
ENTRYPOINT ["bash", "/code/docker-entrypoint.sh"]
