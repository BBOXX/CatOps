"""example.py - example plugin for ChatOps."""

import requests
from catops import CatParser

def ping(argv, params):
    """Check is working."""
    payload = {
        'statusCode':'200',
        'text':'@{} Meow!'.format(params.get('user_name', ['CatOps'])[0]),
        'response_type':'in_channel',
    }
    return payload


def nested(argv, params):
    """This is an implementation of a nested argument parser. e.g. git --help, git status --help """
    parser = CatParser(
        description='Check plugin loader is working',
        usage='''meow hi''')
    # take from second argument since are in the 2nd level of the argument parsing.
    args = parser.parse_args(argv[1:])
    payload = {
        'statusCode':'200',
        'text':'args were: {}'.format(argv),
        'response_type':'in_channel',
        'headers':{'Content-Type': 'application/json'}
    }
    return payload


def cat(argv, params):
    # Print prints logs to cloudwatch
    # Send response to response url
    caturl = 'http://thecatapi.com/api/images/get?format=xml&size=med&type=jpg,png&results_per_page=1'
    start = '<url>'
    end = '</url>'
    catr = requests.get(caturl)
    cattext = catr.text
    url = (cattext.split(start))[1].split(end)[0] 

    payload = {
        'statusCode':'200',
        "attachments": [
            {
                "author_name": '@{} /catops cat'.format(params.get('user_name', ['CatOps'])[0]),
                "fallback": "Meow meow.",
                "title": "Meow!",
                "text": "Here is a cat.",
                "image_url": url,
                "color": "#764FA5"
            }
        ],
        'response_type':'in_channel',
        'headers':{'Content-Type': 'application/json'}
    }
    return payload


def dog(argv, params):
    # Print prints logs to cloudwatch
    # Send response to response url
    dogurl = 'https://api.thedogapi.com/v1/images/search?breed_id=&mime_types=jpg,png&limit&format'
    dogr = requests.get(dogurl)
    url = dogr.json()[0].get('url')

    payload = {
        'statusCode':'200',
        "attachments": [
            {
                "author_name": '@{} /catops dog'.format(params.get('user_name', ['CatOps'])[0]),
                "fallback": "Woof woof.",
                "title": "Woof!",
                "text": "Evil doggo.",
                "image_url": url,
                "color": "#764FA5"
            }
        ],
        'response_type':'in_channel',
        'headers':{'Content-Type': 'application/json'}
    }
    return payload
