import json
from decimal import Decimal


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)

        return json.JSONEncoder.default(self, obj)


def build_response(status_code, body=None):
    response = {
        'statusCode': status_code,
        'headers': {
            'Content_Type': 'application/json',
            'Access-Control-Allow-origin': '*'
        }
    }
    if body:
        response['body'] = json.dumps(body, cls=CustomEncoder)

    return response