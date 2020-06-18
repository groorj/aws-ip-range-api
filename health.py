import json

# create response
def create_response(status_code, message):
    return {
        'statusCode': str(status_code),
        'body': json.dumps({ "message": message }),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            },
        }

# main
def check(event, context):
    return create_response(200, "Success")

# End;