#/bin/python3
"""Handlers for AWS Lambda."""
import datetime
import json
from catops import (
    get_slack_colour,
    create_slack_attachment
)
from slacker import Slacker

with open('tokens.json', 'r') as stream:
    TOKENS = json.load(stream)

SLACK = Slacker(TOKENS['SlackBotOAuthToken'])


def log(event, context):
    """Print logs to Slack (maybe after some processing)"""
    body = event.get('body')
    request_context = event.get("requestContext")
    identity = request_context.get('identity')
    source_ip = identity.get('sourceIp')

    # SLACK.chat.post_message('#bot_tests', body)
    err = False
    try:
        jbody = json.loads(body)
        message = jbody.get('message')
        time = jbody.get('time')
        level = jbody.get('level')
        channels = jbody.get('channels')
    except json.JSONDecodeError:
        message = 'Couldn\'t parse log json, log body:\n{}'.format(body)
        time = str(datetime.datetime.now())
        level = 'WARNING'
        channels = ['#bot_tests']
        err = True

    for channel in channels:
        SLACK.chat.post_message(
            channel,
            attachments=[
                create_slack_attachment(
                    text="",
                    fallback=body,
                    author_name="CatOpsLogHandler",
                    color=get_slack_colour(level),
                    fields=[
                        {
                            "title": "Message",
                            "value": message,
                            "short": False if err else True
                        },
                        {
                            "title": "Level",
                            "value": level,
                            "short": True
                        },
                        {
                            "title": "Time",
                            "value": time,
                            "short": True
                        },
                        {
                            "title": "Source IP",
                            "value": source_ip,
                            "short": True
                        },
                    ]
                )])
