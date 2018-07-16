#/bin/python3
"""Handlers for AWS Lambda."""
import json
from slacker import Slacker
SLACK = Slacker('')


def make_response(status_code='200', headers={}, body=''):
    resp = {
        "statusCode": status_code,
        "headers": headers,
        "body": body
    }
    return resp


def log(event, context):
    """Print logs to Slack (maybe after some processing)"""
    SLACK.chat.post_message('#bot_tests', json.dumps(event))
