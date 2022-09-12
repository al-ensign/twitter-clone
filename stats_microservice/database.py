import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import boto3
from boto3.resources.base import ServiceResource


def initialize_db() -> ServiceResource:
    ddb = boto3.resource(
        'dynamodb',
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    return ddb
