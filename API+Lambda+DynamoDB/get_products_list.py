import json
import boto3
products_table = 'cmtr-2848fb67-dynamodb-l-table-products'
stocks_table = 'cmtr-2848fb67-dynamodb-l-table-stocks'

def lambda_handler(event, context):

    uuid = '14ba3d6a-a5ed-491b-a128-0a32b71a38c4'

    if 'headers' in event and 'random-uuid' in event["headers"]:
        uuid += f'-{event["headers"]["random-uuid"]}'

    dynamodb = boto3.client('dynamodb')
    products_key = {
        'id': {'S': uuid}
    }
    stocks_key = {
        'product_id': {'S': uuid}
    }

    products_response = dynamodb.get_item(
        TableName = products_table,
        Key = products_key
    )
    product = products_response.get('Item')

    stocks_response = dynamodb.get_item(
        TableName = stocks_table,
        Key = stocks_key
    )
    stock = stocks_response.get('Item')

    # Combine results
    result = product.copy()
    result['count'] = stock['count']

    return result