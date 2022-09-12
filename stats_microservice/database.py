import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import boto3
from boto3.resources.base import ServiceResource
import settings


class ResourceMeta(type):

    @property
    def resource(cls):
        if not getattr(cls, "_client", None):
            service_name = getattr(cls, "_service_name")
            resource = boto3.resource(
                service_name,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            setattr(cls, "_client", resource)
            return getattr(cls, "_resource")


class DynamoDB(metaclass=ResourceMeta):
    _service_name = 'dynamodb'
