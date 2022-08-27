from project.celery import app
import boto3
from django.conf import settings
import logging


client = boto3.client(
    'ses',
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

verified_sender = settings.DEFAULT_FROM_EMAIL


@app.task
def send_email_to_followers(**kwargs):
    logging.info("Started")
    subject = "New Tweet!"
    recipients = kwargs.get("recipients")
    body = kwargs.get("body")

    logging.info(recipients)
    client.send_email(
        Destination={
            'ToAddresses': recipients,
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': body,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=verified_sender,
    )
    logging.info("Done! Notifications are sent")

