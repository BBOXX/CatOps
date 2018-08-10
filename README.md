<h1 align="center" >CatOps</h1>

Highly trained cats for managing servers.

![Dedicated server support agent.](https://github.com/BBOXX/CatOps/blob/master/docs/catops.jpg)

## What is CatOps

CatOps is a very simple NoOps framework for deploying your own ChatOps bot.

Commands you wish to add to your CatOps implementation are added to a `plugins`
folder in the same directory, and will then be automatically imported and callable
using the function name.

## Why CatOps

- NoOps.
  - Deploy, rewrite, and redeploy FaaS easily with no worrying about setting up and managing servers.
  - Only charged when CatOps is called.

- Codify common maintenance procedures.
  - Perform high level actions without intimate low level knowledge.
  - Prevent errors doing complicated but routine tasks. 

- Unify documentation.
  - CatOps can act as a unified go-to location for help, merging/pooling all documentation into one place.

- Transparency.
  - Team members can see all actions taken by others in solving a problem. Organic learning.
  - No 'go-to' person for certain maintenance tasks.
  - Everyone aware of server changes. No-one surprised that the server is down if they see `/meow restart server` in the chat.
  - Spread knowledge; everyone becomes equally capable of solving problems.
  - Out of date help messages or documentation is more obvious to everyone.

- Context-aware suggestions, suggest actions and display help depending on context.
  - Docs/procedures/etc are useful, but can be too much to read through, hard to find, not up to date. 
  - Reduce clutter when trying to figure out next actions. 

- Reduce context switching.
  - No need for bash, Linux, ssh or VPN to fix most server issues.
  - No checking server logs.
  - Easily accesible and readble output.

- Control access.
  - Only gives necessary access, no unnecessary ssh-ing into production!

## Features

- Completely NoOps. 
- Easily extensible.
- Pay per invocation.
- Provider agnostic.

## Quick Start

1. Install catops `pip install catops`
2. Run `meow install [--template] [--target-dir]`
3. Adjust the template according to your needs e.g. add Slack OAuth tokens, adjust service names etc.
4. Install serverless dependencies `npm install` in the template directory.
5. Run `serverless deploy`
6. Configure your Slack app (i.e. set Slash command/Bot endpoint URLs to appropriate URLs)

## Example

### Handler

Every Lambda function needs a handler, which takes arguments `(event, context)`. In this case, it is necessary to respond instantly to the request with a `200` so the handler below calls the actual functionality asynchronously and then returns a `200` response.

#### Example Handler

```python handler.py
import json
from six.moves.urllib.parse import parse_qs
import requests
import boto3
from catops import convert_dispatch


def respond(event, context):
    """Call handler.main asynchronously and then return instant response."""
    lambda_client = boto3.client('lambda')
    response = {'statusCode':'200'}
    # Call actual function asynchronously
    lambda_client.invoke(
        FunctionName='CatOps-dev-dispatcher',
        InvocationType='Event',
        Payload=json.dumps(event))
    return response


def main(event, context):
    """Main lamda function logic, to be called asynchronously."""
    params = parse_qs(event.get('body'))
    payload = convert_dispatch(params)
    username =  params.get('user_name', ['catops'])[0] 

    # Post to Slack channel
    response_url = params.get('response_url')
    if type(response_url) is list:
        response_url = response_url[0]
    r = requests.post(response_url, data=json.dumps(payload))
    if not r.ok:
        print(r)
        print(r.reason)
        print(r.text)
    return
```

### Plugins

CatOps works around plugins.

- Plugins are python files stored in the 'plugins/' directory.
- CatOps scans this directory for valid functions to import.
- All files and/or functions starting with `_` are ignored. (`_` means they are private and will not be added to the CatOps dispatcher)
- Other functions are added to the CatOps dispatcher and can be called via `/catops <functionname> [argv]`
- All functions need to have the arguments `(argv, params)`
    - argv will contain the arguments passed to the function e.g. for `/catops role --user t.user`, argv will contain `['role', '--user', 't.user']
    - params will contain the parse Lambda event body, which contains all the information from Slack e.g. `{"text": ... , "username": ..., "response_url": ...}`.

#### Example plugin

```python plugins/example.py
"""example.py - example plugin for ChatOps."""
from catops import create_slack_payload

def ping(argv, params):
    """Check is working."""
    text = '@{} Meow!'.format(params.get('user_name', ['CatOps'])[0]),
    return create_slack_payload(text=text)
```

### Serverless configuration

```yaml serverless.yml
service: CatOps

package:
  include:
    - handler.py
    - plugins/**

custom:
  pythonRequirements:
    slim: true

provider:
  name: aws
  stage: ${opt:stage, 'dev'}
  runtime: python3.6
  profile: serverless
  # Permissions for the lambda function
  # If using boto3, ensure correct permissions
  # have been granted to the lambda function
  iamRoleStatements:
    - Effect: Allow
      Action:
        - lambda:InvokeFunction
        - lambda:InvokeAsync
      Resource: "*"

functions:
  dispatcher:
    handler: handler.main
  respond:
    handler: handler.respond
    events:
      - http:
          path: ping
          method: post

plugins:
  - serverless-python-requirements
```

### Deploy and Test

```bash
serverless deploy
serverless invoke --function dispatcher --path /path/to/json/data --log
```

See [examples](https://github.com/BBOXX/CatOps/tree/master/examples) and [templates](https://github.com/BBOXX/CatOps/tree/master/catops/templates) for more.

## Useful functions

```python
# auth.py
def verify_request(event, slack_secret, timeout=True):
    """Verify that Lambda event came from Slack"""

def get_user_slack(event, oauth, team_id=None, channel_id=None):
    """Check whether user exists and is in specified team and channel.

    Arguments:
        event       - AWS Lambda event
        oauth       - Slack OAUTH token
        team_id     - Slack team_id (workspace, i.e. BBOXX)
        channel_id  - Channel user must be in
    Returns:
        False, err_msg
        True, user_dict with id, name, team_id, channel_id, email
    """

# dispatcher.py
def dispatch(command, params=None, plugin_dir='plugins/'):
    """Create Dispatcher object and run parse_command on (command, params)"""
 
# helpers.py
def get_slack_colour(level):
    """Return Slack colour value based on log level."""

def get_text(params):
    """Return event_text from parse_qs event.get('body')."""

def create_slack_attachment(fallback=None,
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

def create_slack_payload(response_type='ephemeral', text="", attachments=None):
    """Create a Slack payload formatted correctly."""

def convert_dispatch(params, convert_function=None, plugin_dir='plugins/'):
    """Call dispatch and convert the output accordingly into a payload."""

# slack_handler.py

class SlackHandler(logging.Handler):
    """Logger slack_handler which posts json log body to lambda_url."""

# install.py

def install(argv=None):
    """Install catops serverless Slack template."""

# parser.py 
class ArgumentParserError(Exception):
    """Error raised by ArgumentParser"""
    pass


class CatParser(argparse.ArgumentParser):
    """Overrides error method to throw an error instead of exiting"""
    def error(self, message):
        raise ArgumentParserError(message)

```

## Installation

```bash
sudo apt-get install npm
sudo npm install -g serverless
npm install serverless-python-requirements
pip install catops
```

Install `serverless-python-requirements` in the same dir as `serverless.yml`.

## Limitations

- Passive rather than active; needs to be triggered (e.g. by Slack slash commands (could run it every command))
- Limitations of FaaS
  - Max size (256MB for AWS Lambda)
  - Execution time limit (5 minute for AWS Lambda)
  - No state (recommend using a cloud-based database for state e.g. DynamoDB for AWS)
- No autocomplete inside of Slack.

