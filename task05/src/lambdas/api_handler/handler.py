import boto3
import uuid
import json
import datetime

table_name = 'Events'

def lambda_handler(event, context):

    body = event
    principal_id = body['principalId']
    content = body['content']

    event_id = str(uuid.uuid4())
    created_at = datetime.datetime.today().isoformat()
    
    item = {
        'id': event_id,
        'principalId': int(principal_id),
        'createdAt': created_at,
        'body': content
    }

    dynamodb = boto3.client('dynamodb')

    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )

    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }

