import json
import requests
import boto3
from catops import dispatch
from six.moves.urllib.parse import parse_qs


def make_response(err, res=None):
    if res and (isinstance(res, dict) or isinstance(res, list)):
        res = json.dumps(res)
    payload = {
        'statusCode':'400' if err else '200',
        'body':err.message if err else res,
        'headers':{'Content-Type': 'application/json'},
    }
    return payload


def respond(event, context):
    lambda_client = boto3.client('lambda')
    response = make_response(None, 'Meow!')
    # Call actual function asynchronously
    print(lambda_client.list_functions())
    lambda_client.invoke(
        FunctionName='CatOpsAsyncTest-dev-dispatcher',
        InvocationType='Event',
        Payload=json.dumps(event))
    return response


def execute(text):
    s = None
    err = None
    try:
        s = dispatch(text)
    except Exception as error:
        err = error
    return respond(s, '')


def func(event, context):
    # Print prints logs to cloudwatch
    print(event)
    if not isinstance(event, dict):
        try:
            event = json.loads(event)
        except:
            pass

    params = parse_qs(event.get('body'))
    print(params)
    # Send response to response url
    payload = {
        'statusCode':'200',
        'text':'Delayed response',#{'text':'Delayed response.'},
        'headers':{'Content-Type': 'application/json'}
    }
    # Post to Slack channel
    r = requests.post(params.get('response_url')[0], data=json.dumps(payload))
    print(r)
    if not r.ok:
        print(dir(r))
        print(r.reason)
        print(r.text)
        print(r.json)
    return


if __name__ == '__main__':
    text = 'meow hi'
    print(execute(text))
