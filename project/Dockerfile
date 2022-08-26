FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile /app/
COPY Pipfile.lock /app/


RUN apt-get update && apt-get install -y netcat

#RUN apt-get update \
#    && apt-get add postgresql-dev gcc python3-dev musl-dev libffi-dev bash \

#RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
#RUN pip install --upgrade pip
RUN pip install pipenv

RUN pipenv install --system --deploy --ignore-pipfile

COPY . /app

RUN chmod a+x /app/entrypoint.sh

COPY . .

#ENTRYPOINT ["sh", "/app/entrypoint.sh"]
