from project.celery import app
import boto3
from django.conf import settings
import logging
from users.aws import SESClient


verified_sender = settings.DEFAULT_FROM_EMAIL


@app.task
def send_email_to_followers(**kwargs):
    logging.info("Started")
    subject = "New Tweet!"
    recipients = kwargs.get("recipients")
    body = kwargs.get("body")

    logging.info(recipients)
    SESClient.send_email(
        recipients,
        verified_sender,
        body,
        subject,
    )
    logging.info("Done! Notifications are sent")

