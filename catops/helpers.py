"""CatOps related helpers. Response creator, attachment colours."""
import json
from .dispatcher import dispatch
from .parser import ArgumentParserError


def get_slack_colour(level):
    """Return Slack colour value based on log level."""
    level = level.upper()
    colours = {
        "CRITICAL": "ff0000",
        "ERROR": "ff9933",
        "WARNING": "ffcc00",
        "INFO": "33ccff",
        "DEBUG": "good"
    }
    return colours.get(level, "good")


def get_text(params):
    """Return event_text from parse_qs event.get('body')."""
    event_text = params.get('text')
    if not event_text:
        event_text = 'help'
    elif isinstance(event_text, list):
        event_text = event_text[0]
    elif isinstance(event_text, str):
        pass
    else:
        event_text = str(event_text)
    return event_text


def create_slack_attachment(fallback,
                            color=None,
                            pretext=None,
                            author_name=None,
                            author_link=None,
                            author_icon=None,
                            title=None,
                            title_link=None,
                            text=None,
                            fields=None,
                            image_url=None,
                            thumb_url=None,
                            footer=None,
                            footer_icon=None,
                            ts=None
    ):
    """Create slack attachment payload
    See https://api.slack.com/docs/message-attachments for more info.
    
    Arguments:
        fallback - Required plain-text summary of the attachment
        [color] - Colour of the attachment
        [pretext] - Optional text that appears above the attachment block
        [author_name]
        [author_link]
        [author_icon] - URL to author icon
        [title] - Title of the attachment
        [title_link]
        [text] - Optional text that appears inside the attachment
        [fields] - Array of dicts containing more values
        [image_url] - URL to image attached
        [thumb_url] - URL to image thumbnail
        [footer] - Footer message
        [footer_icon] - URL to footer icon
        [ts] - timestamp
    """
    arguments = locals()  # Must be first line in function
    attachment = {
        key: value
        for key, value in arguments.items()
        if value is not None
    }
    return attachment
    

def create_slack_payload(response_type='ephemeral', text="", attachments=None):
    """Create a Slack payload formatted correctly."""
    payload = {
        'statusCode': '200',
        'headers': {'Content-Type': 'application/json'},
        'response_type': response_type,
        'text': text
    }
    if attachments is not None:
        if isinstance(attachments, dict):
            attachments = [attachments]
        payload['attachments'] = attachments
    return payload


def create_slack_error_payload(title, msg, color):
    attachment = create_slack_attachment(
        fallback="msg",
        title=title,
        text=msg,
        color=get_slack_colour('WARNING')
    )
    err_payload = create_slack_payload(
        response_type='ephemeral',
        attachments=[attachment]
    )
    return err_payload


def convert_dispatch(params, convert_function=None, plugin_dir='plugins/'):
    """Call dispatch and convert the output accordingly into a payload."""
    event_text = get_text(params)
    payload = create_slack_payload('in_channel', text="ERR: Payload didn't get overwritten")
    try:
        retval = dispatch(event_text, params)
        # If retval isn't correctly formatted, make it so
        if convert_function is not None:
            payload = convert_function(retval)
        elif isinstance(retval, str):
            payload = create_slack_payload('in_channel', retval)
        elif isinstance(retval, list):
            payload = create_slack_payload('in_channel', json.dumps(retval))
        elif isinstance(retval, dict):
            if 'statusCode' in retval:
                payload = retval
            else:
                payload = create_slack_payload('in_channel', json.dumps(retval))
        else:
            payload = create_slack_payload('in_channel', str(retval))
    except ArgumentParserError as err:
        title = 'Invalid command: /catops {0}'.format(event_text)
        msg = str(err)
        return create_slack_error_payload(title, msg, get_slack_colour('WARNING'))
    except Exception as err:
        title = 'Kitten dispatch team failed with command: /catops {}'.format(event_text)
        msg = str(err)
        return create_slack_error_payload(title, msg, get_slack_colour('ERROR'))
    return payload


# Keep trying user input until condition is met
def retry_valid_input(
        prompt,
        title='',
        default=None,
        condition=lambda x: x is not None,
        transform=lambda x: x):
    """Keep asking user for input until user input satifies *condition* function.

    Arguments:
        prompt {str} -- User prompt text.

    Keyword Arguments:
        title {str} -- Name of this request for information. (default: {''})
        default {Any} -- Default value of user input. Be careful that default
                         passes condition. (default: {None})
        condition {function: a -> bool} --
                Condition returning boolean to signal correct input from user.
                (default: {lambdax:x is not None})
        transform {function: a -> b} --
                Transformation function transforming user data
                before returning it. (default: {lambda x:x})

    Returns:
        b -- Returns result of transform function (defaults to identity)

    """
    # Fix Python 2.x.
    global input
    try:
        input = raw_input
    except NameError:
        pass

    if default is not None:
        prompt += ' [{}] '.format(default)
    while True:
        user_input = input(prompt) or default
        # If user_input passes the condition, transform and save the output
        if condition(user_input):
            break
        else:
            print('Invalid {}'.format(title))
    return transform(user_input)
