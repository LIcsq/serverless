import unittest
import importlib
from src.lambdas.hello_world.handler import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    def test_hello_endpoint_success(self):
        event = {
            "path": "/hello",
            "httpMethod": "GET"
        }
        expected_response = {
                "statusCode": 200,
                "message": "Hello from Lambda"
            }
        actual_response = lambda_handler(event, None)
        self.assertEqual(actual_response, expected_response)

if __name__ == '__main__':
    unittest.main()

