#!/bin/python3
"""Parse incoming text into commands and dispatch to plugin functions."""

import logging
from .parser import CatParser, ArgumentParserError
from .plugin import find_plugin_files, load_plugin_functions

LOG = logging.getLogger()
LOG.setLevel(logging.WARN)
LOG.addHandler(logging.StreamHandler())


def load_plugins(
        plugin_dir='plugins/',
        ignore_file_prefix='_',
        include_file_prefix='',
        ignore_function_prefix='_',
        include_function_prefix=''):
    """Find plugin files and then load (import & return {name: callable}."""
    # Find files which contain plugins in plugin_dir
    plugin_files = find_plugin_files(
        plugin_dir,
        include_file_prefix,
        ignore_file_prefix)
    # Load functions {name: callable} for each valid function in plugin files
    plugin_functions = load_plugin_functions(
        plugin_files,
        include_function_prefix,
        ignore_function_prefix)
    return plugin_functions


def meow(args=None, params=None):
    """Test function."""
    response = {
        'statusCode': 200,
        'text': '@{} Meow!'.format(params.get('user_name')[0])
    }
    return response


class Dispatcher():
    """Class which maps text commands to imported functions"""
    functions = None    # Dictionary of functions imported from plugins files.
    plugins = None      # Function names.

    def __init__(self, plugin_dir='plugins/'):
        setattr(self, 'meow', meow)
        LOG.info('Loading plugins from %s...', plugin_dir)
        self.plugins, self.functions = load_plugins(plugin_dir)
        if not (self.plugins or self.functions):
            LOG.error('No plugins found.')
            return
        LOG.info(self.plugins)
        for key, val in self.functions.items():
            setattr(self, key, val)
        LOG.info('Plugins loaded.\n')
        return

    def _create_parser(self):
        command_str = ""
        if self.functions is not None:
            func_keys = self.functions.keys()
            func_keys = sorted(list(func_keys))
            command_str = "\n                    ".join(func_keys)
        parser = CatParser(
            usage='''
                <command> [<args>]

                commands:
                    help
                    {0}
            '''.format(command_str),
            add_help=False
        )
        parser.add_argument('command', help='Subcommand to run')
        return parser

    def parse_command(self, text, params):
        """Split space separated text into argv, and run parse_args on it"""
        argv = text.split()
        parser = self._create_parser()
        args = parser.parse_args(argv[0:1])
        if args.command == 'help':
            return parser.format_help()
        if not hasattr(self, args.command):
            err = parser.format_help()
            raise ArgumentParserError(err)
        # use dispatch pattern to invoke method with same name
        return getattr(self, args.command)(argv, params)

    def get_parser(self):
        """Return Dispatcher parser"""
        return self._create_parser()


def dispatch(command, params=None, plugin_dir='plugins/'):
    """Create Dispatcher object and run parse_command on (command, params)"""
    if not params:
        params = {'user_name': ['CatOps']}
    dispatcher = Dispatcher(plugin_dir=plugin_dir)
    return dispatcher.parse_command(command, params)


if __name__ == '__main__':
    dispatch('meow', {'user_name': ['CatOps']})
