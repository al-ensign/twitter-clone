from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource
from boto3.dynamodb.conditions import Key
import logging
import os
import sys
from database import DynamoBase
import settings



sys.path.append(os.path.dirname(os.path.abspath(__file__)))


logger = logging.getLogger(__name__)


class StatsRepository(DynamoBase):
    conf = {
        'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
        'region_name': settings.AWS_REGION
    }

    def __init__(self, conf):
        self.conf = conf
        DynamoBase.__init__(self, self.conf)
        self.table = self.get_table()

    def get_all_pages(self, user_id):
        try:
            response = self.table.query(KeyConditionExpression=Key('user_id').eq(user_id))
        except ClientError as err:
            logger.error(
                "Couldn't query for User's pages. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response["Items"]

    def get_page(self, user_id, page_id):
        try:
            response = self.table.get_item(Key={'user_id': user_id, "page_id": page_id})
            return response.get('Item')
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])

    def add_page(self, page: dict):
        try:
            response = self.table.put_item(Item=page)
        except ClientError as err:
            logger.error(
                "Couldn't add page to table. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response

    def update_page_tweets(self, page: dict):
        response = self.table.update_item(
            Key={'user_id': page.get('user_id'), "page_id": page.get("page_id")},
            UpdateExpression="""
                set
                    tweets=:tweets,
                    likes=:likes
            """,
            ExpressionAttributeValues={
                ':tweets': page.get('tweets'),
                ':likes': page.get('likes'),
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def update_page_full(self, page: dict):
        response = self.table.update_item(
            Key={'user_id': page.get('user_id'), "page_id": page.get("page_id")},
            UpdateExpression="""
                set
                    followers=:followers,
                    follow_requests=:follow_requests,
                    tweets=:tweets,
                    likes=:likes,
                    is_blocked=:is_blocked            
            """,
            ExpressionAttributeValues={
                ':followers': page.get('followers'),
                ':follow_requests': page.get('follow_requests'),
                ':tweets': page.get('tweets'),
                ':likes': page.get('likes'),
                ':is_blocked': page.get('is_blocked'),
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_page(self, user_id, page_id):
        response = self.table.delete_item(
            Key={'user_id': user_id, 'page_id': page_id}
        )
        return response


conf = {
        'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
        'region_name': settings.AWS_REGION
    }

dynamo = StatsRepository(conf)
