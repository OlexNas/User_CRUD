from custom import build_response
import boto3
import json

dynamo_db_table_name = 'user_crud_1'
dynamo_db = boto3.resource('dynamodb')
table = dynamo_db.Table(dynamo_db_table_name)


def register(request_body):
    name = request_body['name']
    email = request_body['email']
    password = request_body['password']

    user = {
        'name': name,
        'email': email,
        'password': password
    }
    save_user(user)

    register_body = {
        'Operation': 'Save',
        'Message': 'Success',
        'Item': user
    }

    return build_response(200, register_body)


def save_user(user):
    check_user = json.loads(get_user(user)['body'])
    if not 'name' in check_user:
        table.put_item(Item=user)

        body = {
            'Operation': 'Save',
            'Message': 'Success',
            'Item': user
        }

        return build_response(200, body)
    else:
        return build_response(401, {
            'Message': f"User {user['name']} already exist..."
        })


def delete_user(request_body):
    name = request_body['name']
    check_user = json.loads(get_user(request_body)['body'])

    if 'name' in check_user:
        response = table.delete_item(
            Key={
                'name': name
            },
            ReturnValues='ALL_OLD'
        )

        body = {
            'Operation': 'Delete',
            'Message': 'Success',
            'User': response
        }

        return build_response(200, body)
    else:
        return build_response(401, {
            'Message': f'User {name} not found'
        })


def get_user(request_body):
    name = request_body['name']
    response = table.get_item(
        Key={
            'name': name
        })
    if 'Item' in response:
        return build_response(200, response['Item'])

    else:
        return build_response(401, {
            'Message': "User doesn't exist"
        })


def get_users():
    response = table.scan(
        TableName=dynamo_db_table_name
    )['Items']

    if response:
        return build_response(200, response)
    else:
        return build_response(401, {
            'Message': 'No users'
        })


def update_user(request):
    name = request['name']
    update_key = request['update_key']
    update_value = request['update_value']
    user = json.loads(get_user(request)['body'])

    if 'name' in user:
        if update_key in user:
            response = table.update_item(
                Key={
                    'name': name
                },
                UpdateExpression=f'set {update_key} = :value',
                ExpressionAttributeValues={
                    ':value': update_value
                },
                ReturnValues='UPDATED_NEW'
            )

            body = {
                'Operation': 'Update',
                'Message': 'Success',
                'UserAttr': response
            }
            return build_response(200, response)
        else:
            return build_response(401, {
                'Message': f'There is no {update_key} in user'
            })
    else:
        return build_response(401, {
            'Message': 'User Does not exist...'
        })

