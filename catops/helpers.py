"""CatOps related helpers. Response creator, attachment colours."""
import json
from .dispatcher import dispatch
from .parser import ArgumentParserError


def get_slack_colour(level):
    """Return Slack colour value based on log level."""
    colour = "good"
    level = level.upper()
    if level == "CRITICAL":
        colour = "ff0000"
    if level == "ERROR":
        colour = "ff9933"
    elif level == "WARNING":
        colour = "ffcc00"
    elif level == "INFO":
        colour = "33ccff"
    elif level == "DEBUG":
        colour = "good"
    return colour


def get_text(params):
    event_text = params.get('text')
    if not event_text:
        event_text = 'help'
    elif type(event_text) is list:
        event_text = event_text[0]
    elif type(event_text) is str:
        pass
    else:
        event_text = str(event_text)
    return event_text


def convert_dispatch(params, convert_function=None):
    """Call dispatch and convert the output accordingly into a payload."""
    payload = {
        'statusCode': '200',
        'headers':{'Content-Type':'application/json'}
    }

    try:
        event_text = get_text(params)
        retval = dispatch(event_text, params)
        if convert_function is not None:
            payload = convert_function(retval)
        elif type(retval) is str:
            payload['text'] = retval
        elif type(retval) is list: 
            payload['text'] = json.dumps(retval)
        elif type(retval) is dict:
            if 'statusCode' in retval:
                payload = retval
            else:
                payload['text'] = json.dumps(retval)
        else:
            payload['text'] = str(retval)
    except ArgumentParserError as err:
        title = 'Invalid command: /catops {0}'.format(event_text)
        msg = '{1}'.format(event_text, err)
        payload['attachments'] = [{
            'title':title,
            'text':msg,
            'color':get_slack_colour('WARNING')
        }]
    except Exception as err:
        title = 'Kitten dispatch team failed with command: /catops {}'
        msg = err
        payload['attachments'] = [{
            'title':title,
            'text':msg,
            'color':get_slack_colour('ERROR')
        }]
    return payload

