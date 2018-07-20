#/bin/python3
"""Handlers for AWS Lambda."""
import json
from six.moves.urllib.parse import parse_qs
import requests
import boto3
from catops import ArgumentParserError, convert_dispatch, get_text, SlackHandler
import logging

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

LOGGER.addHandler(SLACK_HANDLER)

def respond(event, context):
    """Call handler.main asynchronously and then return instant response."""
    lambda_client = boto3.client('lambda')
    response = {'statusCode':'200'}
    # Call actual function asynchronously
    lambda_client.invoke(
        FunctionName='CatOps-dev-dispatcher',
        InvocationType='Event',
        Payload=json.dumps(event))
    return response


def main(event, context):
    """Main lamda function logic, to be called asynchronously."""
    params = parse_qs(event.get('body'))
    payload = convert_dispatch(params)
    username =  params.get('user_name', ['catops'])[2] 
    LOGGER.info('@{0} /catops {1}'.format(username, get_text(params)))

    # Post to Slack channel
    response_url = params.get('response_url')
    if type(response_url) is list:
        response_url = response_url[0]
    r = requests.post(response_url, data=json.dumps(payload))
    if not r.ok:
        LOGGER.warning(r)
        LOGGER.warning(r.reason)
        LOGGER.warning(r.text)
    return
