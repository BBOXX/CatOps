# CatOps
Highly trained cats for managing servers.

## Table of Contents

## Features

- Completely NoOps. 
- Easily add commands.
- Pay per invokation.
- Provider agnostic.

## Example

## FAQ

## Installation

### Install node
https://www.metachris.com/2017/01/how-to-install-nodejs-6-lts-on-ubuntu-and-centos/

### Install serverless


# Old readme
For now, research on implementing an event-driven, serverless ChatOps integration (for Slack) that is capable of managing DevOps.

## Why

1. No switching into Shell/Linux/ssh/VPN to fix server issues. (ideally)
2. Common procedures/commands codified. Gives capability for high level actions to be completed by a broader range of staff. e.g. reset database connections. Staff may know *what* to do but not how to do it exactly (or will fumble through it).
3. Context-aware suggestions. Docs/procedures/etc are useful, but can be too much to read through, hard to find, not up to date. Can suggest possible actions depending on context.
4. Prevents errors when (late at night e.g.) completing complicated/multistage but routine tasks.
5. Processes that cannot be codified can be automated (e.g. a rota, chatbot can assign responsibility).
6. Output easily readable and accessible during downtime periods (no checking server logs necessary in most cases).
7. Transparency to all members what is going on.
8. Only giving necessary access (e.g. only functions to perform not ssh access to production)

9. Serves as a great example of NoOps/serverless infrastructure for future application

## Limitations

1. Limitations of Lambda (5 min max time)
2. Won't have covered all edge cases

## Specification

### ChatOps itself must be as close to NoOps as possible, since when it becomes mission critical it needs to always be up.

1. Low Ops (serverless/auto-deploy/very easily deployed)
2. Slack compatible
3. Interactive (interruptable, responds to Slack)
4. Triggers on cloudwatch/uptime robot events
5. Logs clearly

## Infrastructure

### Mark 1

Note: Can use existing chatbot code.

1. Automatically provision low resource (EC2, elastic beanstalk?) listener server to listen on Slack. (Can Lambda/serverless functions be triggered by Slack message themselves, or is there an App that can create event triggers already that can just trigger Lambdas?
2. LS (Listener Server) manages triggering/provisioning of various asynchronous Lambdas.
3. One Listener Server for entire QuackOps deploy? (Very low load, just needs to execute like a switch almost.)
4. LS sends slack data to Lambdas for parsing.
5. LS receives data/logging from serverless components for posting in Slack.

### Mark 2

1. Slack 'slash' command set-up.
2. Text sent to API Gateway (or directly to DD) which forwards to decoder/dispatcher Lambda.
3. DD (Decoder/Dispatcher Lambda) triggers relevant Lambda function.
4. DynamoDB exists for state.
5. Lambda functions post to Slack channel and listen for asynchronous responses via API Gateway/DynamoDB.

### Properties

1. Pay per function
    1. Every time you parse Slack text.
    2. Every time text is valid, call another Lambda.
2. Asynchronous (property of being serverless)
    1. Easily set in motion many Lambda's to be executed from a low load LS (e.g. parse as much text as necessary and pay per use instead of fixed).
3. Interruptable (could be difficult due to asynchronous)
4. Persistent server (LS) would be a fixed cost but aimed to be low load.
