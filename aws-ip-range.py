import json
import logging
import os
import inspect
import urllib
import urllib.request
from ipaddress import ip_network, ip_address

# logger
logger = logging.getLogger()
logger_level = logging.getLevelName(os.environ['LOGGER_LEVEL'])
logger.setLevel(logger_level)

# validate access
def validate_access(event, context):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    logger.debug("RESTRICTED_ACCESS_ENABLED: [%s]", os.environ['RESTRICTED_ACCESS_ENABLED'])
    error_message = "You are not allowed, get out!"
    if os.environ['RESTRICTED_ACCESS_ENABLED'] == 'true':
        logger.info("Restricted access is enabled")
        if os.environ['RESTRICTED_ACCESS_HTTP_HEADER'] in event["headers"]:
            logger.info("Value for header [%s] is: [%s]", os.environ['RESTRICTED_ACCESS_HTTP_HEADER'], event["headers"][os.environ['RESTRICTED_ACCESS_HTTP_HEADER']])
        else:
            logger.error("RESTRICTED_ACCESS_ENABLED is enabled and HTTP header was not provider")
            logger.debug("http headers: [%s]", event["headers"])
            http_code = 400
            error_message = "RESTRICTED_ACCESS_ENABLED is enabled. You must provide HTTP header for authentication."
            raise ValueError(http_code, error_message)

        if event["headers"][os.environ['RESTRICTED_ACCESS_HTTP_HEADER']] != os.environ['RESTRICTED_ACCESS_SECRET']:
            logger.error("Key provided is not valid")
            logger.debug("Error: [%s]", error_message)
            http_code = 403
            raise ValueError(http_code, error_message)
        else:
            logger.info("Key provided is valid")
    else:
        logger.info("Restricted access is NOT enabled")

# create response
def create_response_new(status_code, message_body):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    return {
        'statusCode': str(status_code),
        'body': json.dumps(message_body),
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

# entry point -> return all data
def get_all_data(event, context):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    return_info_final = {}
    # validate the access to this resource
    try:
        validate_access(event, context)
    except ValueError as err:
        return_info_final['request'] = { "request_status": "Fail", "error_message": err.args[1], "http_error_code": err.args[0] }
        return create_response_new(err.args[0], return_info_final)
    ip = event['pathParameters']['ip']
    logger.debug("IP: [%s]", ip)
    data = 'unknown'
    http_code = 404
    ip_data = get_ip_range_json()
    prefixes = ip_data['prefixes']
    my_ip = ip_address(ip)
    for prefix in prefixes:
        if my_ip in ip_network(prefix['ip_prefix']):
            data = prefix
            http_code = 200
    return_info_final['request'] = { "request_status": "Success", "data": data, "http_error_code": http_code }
    return create_response_new(http_code, return_info_final)

# entry point -> return region
def get_region(event, context):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    return_info_final = {}
    # validate the access to this resource
    try:
        validate_access(event, context)
    except ValueError as err:
        return_info_final['request'] = { "request_status": "Fail", "error_message": err.args[1], "http_error_code": err.args[0] }
        return create_response_new(err.args[0], return_info_final)
    ip = event['pathParameters']['ip']
    logger.debug("IP: [%s]", ip)
    region = 'unknown'
    http_code = 404
    ip_data = get_ip_range_json()
    prefixes = ip_data['prefixes']
    my_ip = ip_address(ip)
    for prefix in prefixes:
        if my_ip in ip_network(prefix['ip_prefix']):
            region = prefix['region']
            http_code = 200
    return_info_final['request'] = { "request_status": "Success", "data": region, "http_error_code": http_code }
    return create_response_new(http_code, return_info_final)

# entry point -> return service
def get_service(event, context):
    logger.debug("Inside function: [%s]", inspect.currentframe().f_code.co_name)
    return_info_final = {}
    # validate the access to this resource
    try:
        validate_access(event, context)
    except ValueError as err:
        return_info_final['request'] = { "request_status": "Fail", "error_message": err.args[1], "http_error_code": err.args[0] }
        return create_response_new(err.args[0], return_info_final)
    ip = event['pathParameters']['ip']
    logger.debug("IP: [%s]", ip)
    service = 'unknown'
    http_code = 404
    ip_data = get_ip_range_json()
    prefixes = ip_data['prefixes']
    my_ip = ip_address(ip)
    for prefix in prefixes:
        if my_ip in ip_network(prefix['ip_prefix']):
            service = prefix['service']
            http_code = 200
    return_info_final['request'] = { "request_status": "Success", "data": service, "http_error_code": http_code }
    return create_response_new(http_code, return_info_final)

# End;
