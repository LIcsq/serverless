import boto3
import uuid
import json
import datetime
import os

def lambda_handler(event, context):

    body = event
    principal_id = str(body['principalId'])
    content = str(body['content'])

    event_id = str(uuid.uuid4())
    created_at = datetime.datetime.utcnow().isoformat() + 'Z'
    
    item = {
        'id': {'S': event_id},
        'principalId': {'N': principal_id},
        'createdAt': {'S': created_at},
        'body': {'S': content}
    }

    dynamodb = boto3.client('dynamodb')
    table_name = os.environ['table_name']
    dynamodb.put_item(
        TableName=table_name,
        Item=item
    )

    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "statusCode": 201,
            "event": item
            }, indent=4)
    }

