import boto3
import uuid
import json
import datetime
import os

def lambda_handler(event, context):

    body = event
    principal_id = str(body['principalId'])
    content = {k: v for k, v in body['content'].items()}

    event_id = str(uuid.uuid4())
    created_at = datetime.datetime.utcnow().isoformat() + 'Z'
    
    item = {
        'id': event_id,
        'principalId': principal_id,
        'createdAt': created_at,
        'body': content
    }

    dynamodb = boto3.client('dynamodb')
    table_name = os.environ['table_name']
    dynamodb.put_item(
        TableName=table_name,
        Item={
            'id': {'S': event_id},
            'principalId': {'N': principal_id},
            'createdAt': {'S': created_at},
            'body': {'M': content}
        }
    )

    return {
            "statusCode": 201,
            "body": json.dumps({
                "event": item
            }, indent=4)
        }


string = '{"content": {"name": "John", "surname": "Doe"}}'

