#!/bin/python
"""Install catops template into target directory in command-line style."""
import argparse
import os
from shutil import copy
import sys
import pkg_resources
from catops.helpers import retry_valid_input

DATA_PATH = pkg_resources.resource_filename('catops', 'templates/')


def install(argv=sys.argv):
    """Install catops serverless Slack template."""
    parser = argparse.ArgumentParser(
        usage='meow install [--template] [--target-dir]')
    parser.add_argument('install', help='Install catops template.')

    parser.add_argument(
        '-t', '--template',
        action='store',
        dest='template',
        default='',
        help='Catops template: slash_command, slackbot or slack_logger.')

    parser.add_argument(
        '-d', '--target-dir',
        action='store',
        dest='directory',
        default='',
        help='Dir to install into')

    templates = ['slash_command', 'slackbot', 'slack_logger']
    template_dir = {
        'slash_command': 'aws-slash',
        'slackbot': 'aws-bot',
        'slack_logger': 'slack-logger'
    }

    args = parser.parse_args(argv[1:])
    template = (
        args.template if args.template.lower() in templates else ''
        or
        retry_valid_input(
            'Enter the name of the serverless template',
            title='',
            default='slash_command',
            condition=lambda x: x in templates
        )
    )

    dir_name = args.directory or retry_valid_input(
        'Enter the directory name for your load tests:',
        title='dir',
        default='{}_template'.format(template))

    if template.lower() in templates:
        print('Installing {0} template into {1}'.format(template, dir_name))
        if not os.path.exists(dir_name):
            print('Creating directory {}'.format(dir_name))
            os.makedirs(dir_name)
        else:
            print('{} already exists, skip create directory.'.format(dir_name))
        # Copy files into dir
        files = [
            'handler.py',
            'tokens.json',
            'package.json',
            'package-lock.json',
            'serverless.yml',
            'README.md',
            'requirements.txt'
        ]

        for i, file_path in enumerate(
                map(
                    lambda f: '{0}{1}/{2}'.format(
                        DATA_PATH,
                        template_dir[template],
                        f),
                    files)):

            if os.path.exists(os.path.join(dir_name, files[i])):
                print('{} already exists, skipping copy.'.format(file_path))
            else:
                print('Copying {} into {}'.format(file_path, dir_name))
                copy(file_path, dir_name)
    return 0


if __name__ == '__main__':
    install(sys.argv)
