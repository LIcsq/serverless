from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import boto3
import json
import uuid
import os

_LOG = get_logger('ApiHandler-handler')

client = boto3.client('cognito-idp')
user_pool_name = os.environ['USER_POOL']
'''
dynamodb = boto3.resource('dynamodb')
tables_db = dynamodb.Table(os.environ['TABLES'])
reservations_name = dynamodb.Table(os.environ['RESERVATIONS'])
'''
def signup_post(body):
    username = body['email']
    password = body['password']
    first_name = body['firstName']
    last_name = body['lastName']

    # create the user
    create_user = client.admin_create_user(
        UserPoolId = None,
        Username = username,
        UserAttributes = [
            {
                'Name': 'email',
                'Value': username
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
        MessageAction = 'SUPPRESS'
        )
    _LOG.info(f'{create_user}')
    # set password
    set_password = client.admin_set_user_password(
        UserPoolId=None,
        Username=username,
        Password=password,
        Permanent=True
    )
    _LOG.info(f'{set_password}')
    return {
        'statusCode': 200,
        'body': json.dumps({'status': 200, 'message': 'Signup successful'})
        }

def signin_post(body):
    username = body['email']
    password = body['password']

    client_app = 'client-app'
    user_pools = client.list_user_pools(MaxResults=60)
    for user_pool in user_pools['UserPools']:
        if user_pool['Name'] == user_pool_name:
            user_pool_clients = client.list_user_pool_clients(
                UserPoolId = user_pool['Id'],
                MaxResults = 60
            )
            for user_pool_client in user_pool_clients['UserPoolClients']:
                if user_pool_client['ClientName'] == client_app:
                    client_id = user_pool_client['ClientId']
                    break
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Bad request.')
            }
    
    response_init_auth = client.initiate_auth(
        ClientId = client_id,
        AuthFlow = 'USER_PASSWORD_AUTH',
        AuthParameters = {
            'USERNAME': username,
            'PASSWORD': password
        }
    )

    access_token = response_init_auth['AuthenticationResult']['IdToken']

    return {
        'statusCode': 200,
        'body': json.dumps({'accessToken': access_token})
    }

def tables_get():
    pass

def tables_post():
    pass

def tableId_get():
    pass

def reservations_get():
    pass

def reservation_post():
    pass

def lambda_handler(event, context):

    path = event['path']
    http_method = event['httpMethod']
    body = json.loads(event['body'])
    _LOG.info(f'{path}{http_method}{body}')

    if path == '/signup' and http_method == 'POST':
        #signup_post(body)
        return 'I am work'
        
    elif path == '/signin' and http_method == 'POST':
        response = signin_post(body)
        return response
    
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
