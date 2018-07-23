"""example.py - example plugin for ChatOps."""

import logging
import requests
from catops import CatParser, ArgumentParserError

LOGGER = logging.getLogger('slack_logger')


def ping(argv, params):
    """Check is working."""
    text = '@{} Meow!'.format(params.get('user_name', ['CatOps'])[0])
    return text


def nested(argv, params):
    """This is an implementation of a nested argument parser. e.g git add -h"""
    parser = CatParser(
        description='Check plugin loader is working.',
        usage='''catops nested test''',
        add_help=False)
    parser.add_argument(
        'test',
        help="Test argument. Enter 'help' to see help message.")
    help_msg = parser.format_help()
    try:
        # second argument since are in the 2nd level of the argument parsing.
        args = parser.parse_args(argv[1:])
        payload = {
            'statusCode': '200',
            'text': 'args were: {}'.format(argv),
            'response_type': 'in_channel',
            'headers': {'Content-Type': 'application/json'}
        }

        if args.test != 'test' or args.test == 'help':
            payload['text'] = '{0}\n{1}'.format(
                payload['text'],
                help_msg)

    except ArgumentParserError as err:
        msg = '{0}\n{1}'.format(err, help_msg)
        payload = {
            'statusCode': '200',
            'text': msg,
            'response_type': 'ephemeral',
            'headers': {'Content-Type': 'application/json'}
        }
    return payload


def cat(argv, params):
    """Returns a slack attachment with a picture of a cat from thecatapi"""
    # Print prints logs to cloudwatch
    # Send response to response url
    caturl = 'http://thecatapi.com/api/images/get?format=xml&size=med&type=jpg,png&results_per_page=1'
    start = '<url>'
    end = '</url>'
    catr = requests.get(caturl)
    cattext = catr.text
    url = (cattext.split(start))[1].split(end)[0]

    payload = {
        'statusCode': '200',
        "attachments": [
            {
                "author_name": '@{} /catops cat'.format(
                    params.get('user_name', ['CatOps'])[0]),
                "fallback": "Meow meow.",
                "title": "Meow!",
                "text": "Here is a cat.",
                "image_url": url,
                "color": "#764FA5"
            }
        ],
        'response_type': 'in_channel',
        'headers': {'Content-Type': 'application/json'}
    }
    return payload


def dog(argv, params):
    """Returns a slack attachment with a picture of a dog from thedogapi"""
    # Print prints logs to cloudwatch
    # Send response to response url
    dogurl = 'https://api.thedogapi.com/v1/images/search?mime_types=jpg,png'
    dogr = requests.get(dogurl)
    url = dogr.json()[0].get('url')

    payload = {
        'statusCode': '200',
        "attachments": [
            {
                "author_name": '@{} /catops dog'.format(
                    params.get('user_name', ['CatOps'])[0]),
                "fallback": "Woof woof.",
                "title": "Woof!",
                "text": "Evil doggo.",
                "image_url": url,
                "color": "#764FA5"
            }
        ],
        'response_type': 'in_channel',
        'headers': {'Content-Type': 'application/json'}
    }
    return payload
