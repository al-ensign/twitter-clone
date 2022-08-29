import json

import boto3
from django.conf import settings


s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)

bucket = settings.AWS_STORAGE_BUCKET_NAME


def get_presigned_url(file_name, method):
    presigned_url = s3.generate_presigned_url(
        ClientMethod=method,
        Params={
            'Bucket': bucket,
            'Key': file_name,
        },
        ExpiresIn=3600
    )

    data = json.dumps({
        'data': presigned_url,
        'url': 'https://%s.s3.amazonaws.com/%s' % (bucket, file_name),
    })

    return data

