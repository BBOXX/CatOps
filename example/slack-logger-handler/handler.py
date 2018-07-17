#/bin/python3
"""Handlers for AWS Lambda."""
import json
from slacker import Slacker
SLACK = Slacker('')

def log(event, context):
    """Print logs to Slack (maybe after some processing)"""
    body = event.get('body')
    request_context = event.get("requestContext")
    identity = request_context.get('identity')
    source_ip = identity.get('sourceIp')

    def get_colour(level):
        """Return Slack colour value based on log level."""
        colour = "good"
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

    # SLACK.chat.post_message('#bot_tests', body)
    jbody = json.loads(body)
    message = jbody.get('message')
    time = jbody.get('time')
    level = jbody.get('level')
    channels = jbody.get('channels')
    for channel in channels:
        SLACK.chat.post_message(
            channel,
            attachments=[
                {
                    "text":"",
                    "fallback":body,
                    "author_name":"CatOpsLogHandler",
                    "color":get_colour(level),
                    "fields":[
                        {
                            "title":"Message",
                            "value":message,
                            "short":True
                        },
                        {
                            "title":"Level",
                            "value":level,
                            "short":True
                        },
                        {
                            "title":"Time",
                            "value":time,
                            "short":True
                        },
                        {
                            "title":"Source IP",
                            "value":source_ip,
                            "short":True
                        },
                    ]
                }])
