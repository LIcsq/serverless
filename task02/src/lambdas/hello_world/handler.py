def lambda_handler(event, context):
    path = event.get('path', '')
    method = event.get('httpMethod', '')
    try:
        if path == '/hello' and method == 'GET':
            response = {
                "statusCode": 200,
                "message": "Hello from Lambda"
            }
    except Exception as e:
        response = {
            "statusCode": 400,
            "message": f"Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}"
        }
    return response
