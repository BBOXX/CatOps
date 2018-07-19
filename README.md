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

## Example

### Python handler

```python handler.py
import json
from six.moves.urllib.parse import parse_qs
import requests
import boto3
from catops import dispatch

def respond(event, context):
    """Call handler.main asynchronously and then return instant response."""
    lambda_client = boto3.client('lambda')
    response = {'statusCode':'200'}
    # Call actual function asynchronously
    lambda_client.invoke(
        FunctionName='CatOpsAsyncTest-dev-dispatcher',
        InvocationType='Event',
        Payload=json.dumps(event))
    return response

def main(event, context):
    """Main lamda function logic, to be called asynchronously."""
    # Print prints logs to cloudwatch
    print(event)
    params = parse_qs(event.get('body'))
    try:
        payload = dispatch(params.get('text')[0], params)
    except Exception as err:
        print("Dispatch failed: {}".format(err))
        payload = {
            'statusCode':'200',
            'text':'Kitten dispatch team did not succeed.',
            'headers':{'Content-Type': 'application/json'}
        }
    # Post to Slack channel
    r = requests.post(params.get('response_url')[0], data=json.dumps(payload))
    if not r.ok:
        print(r)
        print(r.reason)
        print(r.text)
    return
```

### Example plugin

```python plugins/example.py
"""example.py - example plugin for ChatOps."""

def ping(argv, params):
    """Check is working."""
    payload = {
        'statusCode':'200',
        'text':'@{} Meow!'.format(params.get('user_name', ['CatOps'])[0]),
        'response_type':'in_channel',
    }
    return payload
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
  iamRoleStatements:
    - Effect: Allow
      Action:
        - lambda:ListFunctions
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

See [examples](https://github.com/BBOXX/CatOps/tree/master/example) for more.

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

