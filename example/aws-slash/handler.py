#/bin/python3
"""Handlers for AWS Lambda."""
import json
from six.moves.urllib.parse import parse_qs
import requests
import boto3
from catops import ArgumentParserError, convert_dispatch, get_text, SlackHandler
import logging

with open("tokens.json", 'r') as stream:
    TOKENS = json.load(stream)

LOG = logging.getLogger('catops')
LOG.setLevel(logging.INFO)
HANDLER = SlackHandler(TOKENS['SlackLambdaURL'])
HANDLER.setLevel(logging.INFO)
FORMAT = '{\
    "channels":["#bot_tests"],\
    "time":"%(asctime)s", \ "level":"%(levelname)s", \
    "message":"%(message)s"}'
FORMATTER = logging.Formatter(FORMAT)


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
    # Print prints logs to cloudwatch
    LOG.debug(event)
    params = parse_qs(event.get('body'))
    payload = {
        'statusCode':'200',
        'headers':{'Content-Type': 'application/json'}
    }
    payload = convert_dispatch(params)
    LOG.info(payload)

    # Post to Slack channel
    response_url = params.get('response_url')
    if type(response_url) is list:
        response_url = response_url[0]
    r = requests.post(response_url, data=json.dumps(payload))
    if not r.ok:
        LOG.warning(r)
        LOG.warning(r.reason)
        LOG.warning(r.text)
    return
