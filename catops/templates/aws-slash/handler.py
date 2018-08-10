#!/bin/python3
"""Handlers for AWS Lambda."""
import json
import logging
from six.moves.urllib.parse import parse_qs
import requests
from catops import (
    ArgumentParserError,
    convert_dispatch,
    get_text,
    SlackHandler,
    verify_request,
    get_user_slack
)

import boto3

with open('tokens.json', 'r') as stream:
    TOKENS = json.load(stream)

LAMBDA_URL = TOKENS['SlackLambdaURL']

# Custom format to print to #catops_logs
FORMAT = '{\
    "channels":["#catops_logs"],\
    "time":"%(asctime)s", \
    "level":"%(levelname)s", \
    "message":"%(message)s"}'

# Create LOGGER
LOGGER = logging.getLogger('slack_logger')
LOGGER.setLevel(logging.INFO)

# Custom SLACK_HANDLER
SLACK_HANDLER = SlackHandler(lambda_url=LAMBDA_URL)
SLACK_HANDLER.setLevel(logging.INFO)
SLACK_HANDLER.setFormatter(logging.Formatter(FORMAT))
# Stream handler
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(logging.DEBUG)

LOGGER.addHandler(SLACK_HANDLER)
LOGGER.addHandler(STREAM_HANDLER)


def respond(event, context):
    """Call handler.main asynchronously and then return instant response."""
    lambda_client = boto3.client('lambda')
    response = {'statusCode': '200'}
    # Call actual function asynchronously
    LOGGER.debug("Invoking CatOps dispatcher")
    lambda_client.invoke(
        FunctionName='CatOps-dev-dispatcher',
        InvocationType='Event',
        Payload=json.dumps(event))
    return response


def main(event, context):
    """Main lambda function logic, to be called asynchronously."""
    LOGGER.debug("Received invocation from responder")
    params = parse_qs(event.get('body'))
    try:
        payload = convert_dispatch(params)
    except Exception as err:
        LOGGER.error("Error while dispatching: %s", str(err))
    username = params.get('user_name', ['catops'])[0]
    LOGGER.info('@%s /catops %s', username, get_text(params))

    # Post to Slack channel
    response_url = params.get('response_url')
    if isinstance(response_url, list):
        response_url = response_url[0]
    response = requests.post(response_url, data=json.dumps(payload))
    if not response.ok:
        LOGGER.warning(response)
        LOGGER.warning(response.reason)
        LOGGER.warning(response.text)
    return
