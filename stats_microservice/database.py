import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import boto3
from boto3.resources.base import ServiceResource
import settings


class DynamoBase:

    def __init__(self, conf):
        self.conf = conf
        self.table_name = settings.DYNAMODB_TABLE_NAME

        try:
            self.dynamodb = boto3.resource('dynamodb', **conf)
        except Exception as err:
            print("{} - {}".format(__name__, err))
            sys.exit(1)

    def get_table(self):
        return self.dynamodb.Table(self.table_name)




