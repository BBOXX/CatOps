CatOps
======
Highly trained cats for managing servers.

What is CatOps?
---------------

CatOps is a very simple NoOps framework for deploying your own ChatOps bot.

Commands you wish to add to your CatOps implementation are added to a `plugins`
folder in the same directory, and will then be automatically imported and callable
using the function name.

Features
--------

- Completely NoOps. 
- Easily extensible.
- Pay per invocation.
- Provider agnostic.

Why CatOps? (Why ChatOps?)
-------------------------- 

- Codify common maintenance procedures.
		- Perform high level actions without intimate low level knowledge.
		- Prevent errors doing complicated but routine tasks. 

- Unify documentation. Developer docs can be all over the place; CatOps can act as a unified go-to location for help.

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
		- No switching into Shell/Linux/ssh/VPN to fix most server issues.
		- No checking server logs.

- Output easily readable.

- NoOps.
		- Deploy, rewrite, and redeploy FaaS easily with no worrying about setting up and managing servers.
		- Only charged when CatOps is called.

- Control access.
		- Only gives necessary access, no unnecessary ssh-ing into production!


Example
--------

Python handler
^^^^^^^^^^^^^^^

.. code-block:: python

  from catops import dispatch
  import json

  def endpoint(event, context):
      # event = {'command':['meow', 'hi']} # example event passed to lambda
      params = event['command']
      try:
          s = dispatch(params)
      except Exception as err:
          s = str(err)
      response = {
          "statusCode": 200,
          "body": json.dumps(s)
      }
      return response


Example plugin
^^^^^^^^^^^^^^

.. code-block:: python

  """example.py - example plugin for ChatOps."""

  def hi(self):
      return "Meow!"


Serverless configuration
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

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
  runtime: python3.6
  profile: serverless

  functions:
    dispatcher:
      handler: handler.endpoint
      events:
        - http:
            path: ping
            method: get

  plugins:
    - serverless-python-requirements


Deploy and Test
^^^^^^^^^^^^^^^

.. code-block:: bash

  serverless deploy
  serverless invoke --function dispatcher --path /path/to/json/data --log


See examples_ for more.

.. _examples: https://github.com/bboxx/catops/example/

Installation
============

.. code-block:: bash

  sudo apt-get install npm
  sudo npm install -g serverless
  npm install serverless-python-requirements
  pip install catops

Install :code:`serverless-python-requirements` in the same dir as :code:`serverless.yml`.

Limitations
===========

- Passive rather than active; needs to be triggered (e.g. by Slack slash commands)
- Limitations of FaaS
    - Max size (256MB for AWS Lambda)
    - Execution time limit (5 minute for AWS Lambda)
    - No state (recommend using a cloud-based database for state e.g. DynamoDB for AWS)


