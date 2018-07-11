"""example.py - example plugin for ChatOps."""

import argparse

class ArgumentParserError(Exception): pass

class ThrowingParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

def hi(self):
    parser = ThrowingParser(
        description='Check plugin loader is working',
        usage='''meow hi''')
    # prefixing the argument with -- means it's optional
    # now that we're inside a subcommand, ignore the first
    args = parser.parse_args(self.argv[2:])
    return "Meow!"
