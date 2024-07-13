import json
import requests
import boto3
import uuid
import os
from decimal import Decimal

# DynamoDB client
dynamodb = boto3.client('dynamodb')
table =os.environ['table_name']

class OpenMeteoAPI:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    @staticmethod
    def get_weather(latitude, longitude):
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'hourly': 'temperature_2m'
        }
        response = requests.get(OpenMeteoAPI.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()

def lambda_handler(event, context):
    """
    Explain incoming event here
    """
    latitude = event.get('latitude', 52.52)
    longitude = event.get('longitude', 13.419998)

    api_response = OpenMeteoAPI.get_weather(latitude, longitude)
    
    item = {
        'id': str(uuid.uuid4()),
        "forecast": {
            "elevation": api_response['elevation'],
            "generationtime_ms": api_response['generationtime_ms'],
            "hourly": {
                "temperature_2m": api_response['hourly']['temperature_2m'],
                "time": api_response['hourly']['time']
            },
            "hourly_units": {
                "temperature_2m": api_response['hourly_units']['temperature_2m'],
                "time": api_response['hourly_units']['time']
            },
            "latitude": api_response['latitude'],
            "longitude": api_response['longitude'],
            "timezone": api_response['timezone'],
            "timezone_abbreviation": api_response['timezone_abbreviation'],
            "utc_offset_seconds": api_response['utc_offset_seconds']
        }
    }

    item = json.loads(json.dumps(item), parse_float=Decimal)

    # Insert item into DynamoDB
    dynamodb.put_item(TableName=table,
                    Item=item)
    
    return api_response
