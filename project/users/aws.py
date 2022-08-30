import json

import boto3
from django.conf import settings


# s3 = boto3.client(
#     's3',
#     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
# )
#
# # bucket = settings.AWS_STORAGE_BUCKET_NAME
#
#
# def get_presigned_url(file_name, method):
#
#     """
#     Generates a pre-signed url to s3 bucket based on ClientMethod and File_name.
#     """
#
#     presigned_url = s3.generate_presigned_url(
#         ClientMethod=method,
#         Params={
#             'Bucket': bucket,
#             'Key': file_name,
#         },
#         ExpiresIn=3600
#     )
#
#     data = json.dumps({
#         'data': presigned_url,
#         'url': f'https://{bucket}.s3.amazonaws.com/{file_name}',
#     })
#
#     return data


class ClientMeta(type):

    @property
    def client(cls):
        if not getattr(cls,"_client", None):
            service_name = getattr(cls, "_service_name")
            client = boto3.client(
                service_name,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            setattr(cls, "_client", client)
            return getattr(cls, "_client")


class SESClient(metaclass=ClientMeta):
    _service_name = "ses"

    @classmethod
    def send_email(cls, recipients, verified_sender, body, subject):
        cls.client.send_email(
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


class S3Client(metaclass=ClientMeta):
    _service_name = "s3"

    @classmethod
    def get_presigned_url(cls, file_name, method):

        presigned_url = cls.client.generate_presigned_url(
            ClientMethod=method,
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': file_name,
            },
            ExpiresIn=3600
        )

        data = json.dumps({
            'data': presigned_url,
            'url': f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_name}',
        })

        return data





