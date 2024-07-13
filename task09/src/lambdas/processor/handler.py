import json
import requests
import boto3
import uuid
import os

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

    weather_data = OpenMeteoAPI.get_weather(latitude, longitude)
    utc_offset_seconds = 0
    
    item = {
        "id": {'S':str(uuid.uuid4())},
        "forecast": {'M': {
            "elevation": {'S': str(weather_data["elevation"])},
            "generationtime_ms": {'S': str(weather_data['generationtime_ms'])}}},
        "hourly": {'M': {
            "temperature_2m": {'L': [{'S': str(value) for value in weather_data['hourly']['temperature_2m']}]},
            "time": {'L': [{'S': str(value) for value in weather_data["hourly"]["time"]}]}
        }},
        "hourly_units": {'M': {
            "temperature_2m": {'S': weather_data["hourly_units"]["temperature_2m"]},
            "time": {'S': weather_data["hourly_units"]["time"]}
        }},
        "latitude": {'S': str(weather_data["latitude"])},
            "longitude": {'S': str(weather_data["longitude"])},
            "timezone": {'S': weather_data["timezone"]},
            "timezone_abbreviation": {'S': ''.join(weather_data["timezone_abbreviation"])},
            "utc_offset_seconds": {'N': int(utc_offset_seconds)}
        }

    # Insert item into DynamoDB
    dynamodb.put_item(TableName=table,
                    Item=item)
    
    return weather_data
