from catops import dispatch
import json
from six.moves.urllib.parse import parse_qs


def respond(err, res=None):
    return {
            "statusCode":"400" if err else "200",
            "body":err.message if err else json.dumps(res),
            "headers":{"Content-Type": "application/json"},
            }


def execute(text):
    s = None
    err = None
    try:
        s = dispatch(text)
    except Exception as error:
        err = error
    return respond(err, s)


def endpoint(event, context):
    print(event)
    print(event.get('body'))
    params = parse_qs(event["body"])
    print(params)
    response = respond(None, params["text"])
    print(response)
    return response

if __name__=="__main__":
    text = "meow hi"
    print(execute(text))
