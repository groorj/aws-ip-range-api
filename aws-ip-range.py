import json
import logging
import os
import inspect
import urllib
from ipaddress import ip_network, ip_address

# logger
logger = logging.getLogger()
logger_level = logging.getLevelName(os.environ['LOGGER_LEVEL'])
logger.setLevel(logger_level)

# create response
def create_response(status_code, message_content, message_key='key'):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    return {
        'statusCode': str(status_code),
        'body': json.dumps({ message_key: message_content }),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            },
        }

# download ip-range file
def get_ip_range_json():
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)

    response = urllib.request.urlopen(os.environ['IP_RANGE_JSON_URL'])
    json_data = json.loads(response.read())

    return json_data

# handler
def get_region(event, context):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)

    ip = event['pathParameters']['ip']
    logger.debug("IP: [%s]", ip)

    region = 'unknown'
    ip_data = get_ip_range_json()
    prefixes = ip_data['prefixes']
    my_ip = ip_address(ip)
    for prefix in prefixes:
        if my_ip in ip_network(prefix['ip_prefix']):
            region = prefix['region']
            return create_response(200, region, 'region')

# End;