#/bin/python3
"""Handlers for AWS Lambda."""
import json
from six.moves.urllib.parse import parse_qs
import requests
import boto3
from catops import dispatch


def make_response(err, res=None):
    """Make response object for immediate slack response."""
    if res and (isinstance(res, dict) or isinstance(res, list)):
        res = json.dumps(res)
    payload = {
        'statusCode':'400' if err else '200',
        'body':err.message if err else res,
        'headers':{'Content-Type': 'application/json'},
    }
    return payload


def respond(event, context):
    """Call handler.main asynchronously and then return instant response."""
    lambda_client = boto3.client('lambda')
    # response = make_response(None, 'Meow!')
    response = {'statusCode':'200'}
    # Call actual function asynchronously
    lambda_client.invoke(
        FunctionName='CatOpsAsyncTest-dev-dispatcher',
        InvocationType='Event',
        Payload=json.dumps(event))
    return response


def main(event, context):
    """Main lamda function logic, to be called asynchronously."""
    # Print prints logs to cloudwatch
    print(event)
    if not isinstance(event, dict):
        try:
            event = json.loads(event)
        except ValueError as err:
            print(err)

    params = parse_qs(event.get('body'))
    try:
        payload = dispatch(params.get('text')[0], params)
    except Exception as err:
        print("Dispatch failed: {}".format(err))
        payload = {
            'statusCode':'200',
            'text':'Kitten dispatch team did not succeed.',
            'headers':{'Content-Type': 'application/json'}
        }

    # Post to Slack channel
    r = requests.post(params.get('response_url')[0], data=json.dumps(payload))
    if not r.ok:
        print(r)
        print(r.reason)
        print(r.text)
    return
