import boto3
from botocore.exceptions import ClientError

from app.config.enviroment import Settings


def get_dynamodb_client():
    return boto3.client(
        'dynamodb',
        region_name=Settings.REGION,
        endpoint_url=Settings.URL_DATABASE
    )

def create_table(dynamo_client):
    try:
        dynamo_client.create_table(
            TableName='user',
            KeySchema=[
                {
                    'AttributeName': 'user_email',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_email',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        dynamo_client.get_waiter('table_exists').wait(TableName='feedback')
        print("Table created successfully")
    except ClientError as e:
        print(e.response['Error']['Message'])

def delete_table(dynamo_client):
    try:
        dynamo_client.delete_table(TableName='user')
        dynamo_client.get_waiter('table_not_exists').wait(TableName='user')
        print("Table deleted successfully")
    except ClientError as e:
        print(e.response['Error']['Message'])
