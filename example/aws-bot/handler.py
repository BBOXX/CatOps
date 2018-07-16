#/bin/python3
"""Handlers for AWS Lambda."""
import json
from six.moves.urllib.parse import parse_qs
import requests
import boto3
from catops import dispatch
from slacker import Slacker
# from werkzeug.wrappers import Response
SLACK = Slacker('<slack-api-token>')


def make_response(status_code='200', headers={}, body=''):
    resp = {
        "statusCode": status_code,
        "headers": headers,
        "body": body
    }
    return resp


def respond(event, context):
    """Call handler.main asynchronously and then return instant response."""
    lambda_client = boto3.client('lambda')
    print(event)
    body = event.get('body')
    print(body)
    jbody = json.loads(body)
    print(jbody)
    # Call actual function asynchronously
    lambda_client.invoke(
        FunctionName='CatOpsBot-dev-dispatcher',
        InvocationType='Event',
        Payload=body)
    challenge = jbody.get('challenge', False)
    if challenge:
        response = make_response(
                status_code='200',
                headers={'Content-Type':'application/json'},
                body=json.dumps({'challenge':challenge}))
        print(response)
    else:
        response = make_response('200')
    return response


def main(event, context):
    """Main lamda function logic, to be called asynchronously."""
    SLACK.chat.post_message('#bot_tests', json.dumps(event))


def log(event, context):
    """Print logs to Slack (maybe after some processing)"""
    SLACK.chat.post_message('#bot_tests', json.dumps(event))
