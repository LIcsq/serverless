from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import boto3
import json
import uuid
import os

_LOG = get_logger('ApiHandler-handler')

client = boto3.client('cognito-idp')
user_pool_name = os.environ['USER_POOL']
client_app = 'client-app'

user_pool_id = None
response = client.list_user_pools(MaxResults = 60)
for user_pool in response['UserPools']:
    if user_pool['Name'] == user_pool_name:
        user_pool_id = user_pool['Id']
        break
_LOG.info(f'user pool id: {user_pool_id}')

client_app_id = None
response = client.list_user_pool_clients(UserPoolId = user_pool_id)
for user_pool_client in response['UserPoolClients']:
    if user_pool_client['ClientName'] == client_app:
        client_app_id = user_pool_client['ClientId']
        break
_LOG.info(f'Client app id: {client_app_id}')
'''
dynamodb = boto3.resource('dynamodb')
tables_db = dynamodb.Table(os.environ['TABLES'])
reservations_name = dynamodb.Table(os.environ['RESERVATIONS'])
'''


def lambda_handler(event, context):

    path = event['path']
    http_method = event['httpMethod']
    body = json.loads(event['body'])
    _LOG.info(f'{path} {http_method} {body}')

    if path == '/signup' and http_method == 'POST':

        email = body['email']
        first_name = body['firstName']
        last_name = body['lastName']
        password = body['password']
        _LOG.info(f'{email}, {first_name}, {last_name}, {password}')

        response = client.admin_create_user(
            UserPoolId = user_pool_id,
            Username = email,
            UserAttributes = [
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name': 'given_name',
                    'Value': first_name
                },
                {
                    'Name': 'family_name',
                    'Value': last_name
                }
            ],
            TemporaryPassword = password,
            MessageAction = 'SUPRESS'
        )
        _LOG.info(f'Create User Response: {response}')

        response = client.admin_set_user_password(
            UserPoolId = user_pool_id,
            Username = email,
            Password = password,
            Permanent=True
        )
        _LOG.info(f'Set password Response: {response}')

        return {
            'statusCode': 200,
            'body': json.dumps({'Sign-up process is successful'})
        }
        
    elif path == '/signin' and http_method == 'POST':
        email = body['email']
        password = body['password']
        _LOG.info(f'{email}, {password}')

        response = client.initiate_auth(
            AuthFlow = 'USER_PASSWORD_AUTH',
            AuthParameters = {
                'USERNAME': email,
                'PASSWORD': password
                },
            ClientId=user_pool_id,
        )
        accessToken = response['AuthenticationResult']['IdToken']
        _LOG.info(f'accessToken: {accessToken}')
        return {
            'statusCode': 200,
            'body': json.dumps({'accessToken': accessToken})
        }
    
    elif path == '/tables' and http_method == 'GET':
        return "tables GET"
    
    elif path == '/tables' and http_method == 'POST':
        return "tables POST"
    
    elif path == '/tables/{tableId}' and http_method == 'GET':
        tableId = path.split('/')[-1]
        return "tablesId GET"
    
    elif path == '/reservations' and http_method == 'GET':
        return "Reservations GET"
    
    elif path == '/reservations' and http_method == 'POST':
        return "reservations POST"
    
    else:
        return 'No such path'
