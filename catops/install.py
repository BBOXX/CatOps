import os
from shutil import copy
import sys
import pkg_resources

DATA_PATH = pkg_resources.resource_filename('catops', 'example/')

def install(argv=[]):
    """Install catops serverless Slack template."""
    parser = argparse.ArgumentParser(usage='catops template [dir]')
    parser.add_argument('template', help='Catops template to use. slash_command, slackbot or log_handler.')
    parser.add_argument(
        '-d', '--dir',
        action='store',
        dest='directory',
        default='catops_template'
        help='Dir to install into')

    templates = ['slash_command', 'slackbot', 'log_handler']
    args = parser.parse_args(argv)
    if args.template.lower() in templates:
        dir_name = args.directory
        if not os.path.exists(dir_name):
            print("Creating directory {}".format(dir_name))
            os.makedirs(dir_name)
        else:
            print("{} already exists, skipping create directory.".format(dir_name))
        # Copy files into dir
        files = ['handler.py', 'tokens.json', 'package.json', 'package-lock.json', 'serverless.yml', 'README.md', 'requirements.txt']
        for i, file_path in enumerate(map(lambda f: DATA_PATH + f, files)):
            if os.path.exists(os.path.join(dir_name, files[i])):
                print("{} already exists, skipping copy.".format(file_path))
            else:
                print("Copying {} into {}".format(files[i], dir_name))
                copy(file_path, dir_name)
