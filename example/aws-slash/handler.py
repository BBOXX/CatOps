#/bin/python3
"""Handlers for AWS Lambda."""
import json
from six.moves.urllib.parse import parse_qs
import requests
import boto3
from catops import dispatch, ArgumentParserError


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
    print(event)
    params = parse_qs(event.get('body'))
    payload = {
        'statusCode':'200',
        'headers':{'Content-Type': 'application/json'}
    }
    try:
        retval = dispatch(params.get('text')[0], params)
        if type(retval) is str:
            payload['text'] = retval
        elif type(retval) is list: 
            payload['text'] = json.dumps(retval)
        elif type(retval) is dict:
            if all(key in retval for key in ['headers', 'statusCode']):
                payload = retval
            else:
                payload['text'] = json.dumps(retval)
        else:
            payload['text'] = str(retval)
    except ArgumentParserError as err:
        payload['text'] = '{0}\n{1}'.format(params.get('text')[0], err)
    except Exception as err:
        payload['text'] = 'Kitten dispatch team did not succeed\n{}'.format(err)
    # Post to Slack channel
    r = requests.post(params.get('response_url')[0], data=json.dumps(payload))
    if not r.ok:
        print(r)
        print(r.reason)
        print(r.text)
    return
