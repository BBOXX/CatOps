"""dispatch.py Decode & Dispatch: Parse incoming text into commands and dispatch to appropriate plugin functions."""

import logging
from .parser import CatParser, ArgumentParserError
from .plugin import find_plugin_files, load_plugin_functions
import sys
logger = logging.getLogger()
logger.setLevel(logging.WARN)
logger.addHandler(logging.StreamHandler())


def load_plugins(plugin_dir='plugins', ignore_file_prefix='_', include_file_prefix='', ignore_function_prefix='_', include_function_prefix=''):
    plugin_files = find_plugin_files(plugin_dir, include_file_prefix, ignore_file_prefix)
    return load_plugin_functions(plugin_files, include_function_prefix, ignore_function_prefix)

    
def meow(argv=[]):
    """Test function."""
    return "Meow!"


class Dispatcher(object):
    functions = None
    plugins = None
    argv = None

    def __init__(self):
        setattr(self,  'meow', meow)
        logger.info('Loading plugins...')
        self.plugins, self.functions = load_plugins()
        if not (self.plugins or self.functions):
            logger.error('No plugins found.')
            return
        logger.info(self.plugins)
        for key, val in self.functions.items():
            setattr(self, key, val)
        logger.info('Plugins loaded.\n')
        return

    def parse_command(self, text):
        self.argv = text.split()

        parser = CatParser(
            usage='''
                <command> [<args>]

                commands:
                   {0} 
            '''.format("\n".join(self.functions.keys()) if self.functions else None))
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(self.argv[0:1])
        if not hasattr(self, args.command):
            err = 'Unrecognized command: {}'.format(args.command)
            parser.print_help()
            raise ArgumentParserError(err)
        # use dispatch pattern to invoke method with same name
        return getattr(self, args.command)(self.argv)

def dispatch(argv=sys.argv[1:0]):
    d = Dispatcher()
    return d.parse_command(" ".join(argv))

if __name__ == '__main__':
    dispatch()

