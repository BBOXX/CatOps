import argparse

class ArgumentParserError(Exception): pass

class CatParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

