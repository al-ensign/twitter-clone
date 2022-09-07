FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile /app/
COPY Pipfile.lock /app/


RUN apt-get update && apt-get install -y netcat

RUN pip install pipenv

RUN pipenv install --system --deploy --ignore-pipfile

COPY . /app

RUN chmod a+x /app/entrypoint.sh

COPY . .
