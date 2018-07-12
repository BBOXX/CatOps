"""example.py - example plugin for ChatOps."""

from catops import CatParser


def hi(self):
    return "Meow!"


def nested(self):
    """This is an implementation of a nested argument parser. e.g. git --help, git status --help """
    parser = CatParser(
        description='Check plugin loader is working',
        usage='''meow hi''')
    # take from second argument since are in the 2nd level of the argument parsing.
    args = parser.parse_args(self.argv[2:])
    return "Meow!"