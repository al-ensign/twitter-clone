#!/bin/bash


if [ "$RABBIT" = "rabbit" ]
then
    echo "Waiting for rabbit..."

    while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
      sleep 0.1
    done

    echo "Rabbitmq started"
fi

echo "Rabbitmq connected and celery started"

celery -A project worker -l INFO