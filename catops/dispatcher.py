#/bin/python3
"""dispatch.py Decode & Dispatch: Parse incoming text into commands and dispatch to appropriate plugin functions."""

import logging
from .parser import CatParser, ArgumentParserError
from .plugin import find_plugin_files, load_plugin_functions

LOG = logging.getLogger()
LOG.setLevel(logging.WARN)
LOG.addHandler(logging.StreamHandler())


def load_plugins(plugin_dir='plugins', ignore_file_prefix='_', include_file_prefix='', ignore_function_prefix='_', include_function_prefix=''):
    plugin_files = find_plugin_files(plugin_dir, include_file_prefix, ignore_file_prefix)
    return load_plugin_functions(plugin_files, include_function_prefix, ignore_function_prefix)


def meow(args=None, params=None):
    """Test function."""
    return {'statusCode':200, 'text':'@{} Meow!'.format(params.get('user_name')[0])}


class Dispatcher(object):
    functions = None    # Dictionary of functions imported from plugins files.
    plugins = None      # Function names.

    def __init__(self, plugin_dir = 'plugins/'):
        setattr(self,  'meow', meow)
        LOG.info('Loading plugins...')
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
        parser = CatParser(
            usage='''
                <command> [<args>]

                commands:
                    help
                    {0} 
            '''.format("\n                    ".join(self.functions.keys()) if self.functions else ''),
            add_help=False
            )
        parser.add_argument('command', help='Subcommand to run')
        return parser
        
    def parse_command(self, text, params):
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
        return self._create_parser()


def dispatch(command, params={'user_name':['CatOps']}):
    d = Dispatcher()
    return d.parse_command(command, params)

if __name__ == '__main__':
    dispatch('meow', {'user_name':['CatOps']})

