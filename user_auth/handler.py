import logging
from crud import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)


get_method = 'GET'
post_method = 'POST'
patch_method = 'PATCH'
delete_method = 'DELETE'
user_path = '/user'
users_path = '/users'


def crud_lambda(event, context):
    logger.info(event)
    http_method = event['requestContext']['http']['method']
    path = event["rawPath"]

    if http_method == post_method and path == user_path:
        register_body = json.loads(event['body'])
        response = save_user(register_body)

    elif http_method == get_method and path == user_path:
        event_body = json.loads(event['body'])
        response = get_user(event_body)

    elif http_method == patch_method and path == user_path:
        event_body = json.loads(event['body'])
        response = update_user(event_body)

    elif http_method == get_method and path == users_path:
        response = get_users()

    elif http_method == delete_method and path == user_path:
        request_body = json.loads(event['body'])
        response = delete_user(request_body)

    return response



