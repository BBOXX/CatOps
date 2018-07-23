"""Custom parser which raises an error instead of exiting."""
import argparse


class ArgumentParserError(Exception):
    """Error raised by ArgumentParser"""
    pass


class CatParser(argparse.ArgumentParser):
    """Overrides error method to throw an error instead of exiting"""
    def error(self, message):
        raise ArgumentParserError(message)
