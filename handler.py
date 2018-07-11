from catops import dispatch
import json


def execute(params):
    try:
        s = dispatch(params)
    except Exception as err:
        s = str(err)

    response = {
        "statusCode": 200,
        "body": json.dumps(s)
    }

    return response


def endpoint(event, context):
    return execute(event['command'])


if __name__=="__main__":
    event = {'command':['meow', 'hi']}
    print(endpoint(event,''))
