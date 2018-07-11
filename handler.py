from catops import dispatch
import json


def endpoint(event, context):
    try:
        s = dispatch(['meow', 'hi'])
    except Exception as err:
        s = str(err)

    response = {
        "statusCode": 200,
        "body": json.dumps(s)
    }

    return response

if __name__=="__main__":
    print(endpoint('',''))
