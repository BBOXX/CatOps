from catops import dispatch
import json
from six.moves.urllib.parse import parse_qs


def respond(err, res=None):
    return {
        "statusCode": "400" if err else "200",
        "text": err.message if err else json.dumps(res),
        "headers": {
            "Content-Type": "application/json",
        }
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
    return respond(None, {'received':str(event)})
    #params = parse_qs(event["body"])
    #return respond(None, params["text"])

if __name__=="__main__":
    text = "meow hi"
    print(execute(text))
