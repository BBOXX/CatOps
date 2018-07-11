"""dispatch.py Decode & Dispatch: Parse incoming text into commands and dispatch to appropriate plugin functions."""

import argparse
import logging
from .plugin import find_plugin_files, load_plugin_functions
import sys
logger = logging.getLogger()
logger.setLevel(logging.WARN)
logger.addHandler(logging.StreamHandler())

class ArgumentParserError(Exception): pass

class ThrowingParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


def load_plugins(plugin_dir='plugins'):
    return load_plugin_functions(find_plugin_files(plugin_dir, '', '_'), '', '_')


class Dispatcher(object):
    def __init__(self):
        logger.info('Loading plugins...')
        plugins, functions = load_plugins()
        logger.info(plugins)
        for key, val in functions.items():
            setattr(self, key, val)
        logger.info('Plugins loaded.\n')

    def parse_commmand(self, text):
        argv = text.split()

        parser = ThrowingParser(
            usage='''
                quack <command> [<args>]

                commands:
                   {0} 
            '''.format("\n".join(functions.keys())))
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        return getattr(self, args.command)(self)

def dispatch(argv=sys.argv):
    d = Dispatcher()
    return d.parse_command(" ".join(argv))

if __name__ == '__main__':
    dispatch()

