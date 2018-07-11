"""Functions which load plugins."""

import glob
import inspect
import logging
import sys
import os

logger = logging.getLogger(__name__)

def find_plugin_functions(path, include_prefix='', ignore_prefix='_'):
    """
    Import given path and return (docstring, callables) of all functions that pass the test.

    Specifically, the function's ``__doc__`` attribute (a string) and a
    dictionary of ``{'name': callable}`` containing all callables which pass
    the `filter_function` test.
    """
    # Get directory and filename
    directory, filterfile = os.path.split(path)
    # If the directory isn't in the PYTHONPATH, add it so our import will work
    added_to_path = False
    index = None
    if directory not in sys.path:
        sys.path.insert(0, directory)
        added_to_path = True
    # If the directory IS in the PYTHONPATH, move it to the front temporarily,
    # otherwise other locustfiles -- like Locusts's own -- may scoop the intended
    # one.
    else:
        i = sys.path.index(directory)
        if i != 0:
            # Store index for later restoration
            index = i
            # Add to front, then remove from original position
            sys.path.insert(0, directory)
            del sys.path[i + 1]
    # Perform the import (trimming off the .py)
    imported = __import__(os.path.splitext(filterfile)[0])
    # Remove directory from path if we added it ourselves (just to be neat)
    if added_to_path:
        del sys.path[0]
    # Put back in original index if we moved it
    if index is not None:
        sys.path.insert(index + 1, directory)
        del sys.path[0]
    # Return our two-tuple
    def is_function(tup, incl=include_prefix,  ign=ignore_prefix):
        """
        Takes (name, object) tuple, returns True if it's a function.
        """
        name, item = tup
        return bool(
            inspect.isfunction(item)
            and not name.startswith(ign)
            and name.startswith(incl)
        )
    functions = dict(filter(is_function, vars(imported).items()))
    return imported.__doc__, functions


def find_plugin_files(dir_path, include_file_prefix='', ignore_file_prefix='_'):
    """Searches the directory at *dir_path* and subdirectories for all
    functions starting with *include_file_prefix* not starting with *ignore_file_prefix*
    and specified by func, finds and imports all functions and returns
    dictionary with name and function callable.

    Arguments:
        dir_path {string} -- path to the directory to import function.
        func {function} -- returns a tuple of the ``__doc__`` attribute (a string) &
                           dictionary of ``{'name': callable}`` of the functions.
        include_file_prefix {string} -- Include only files starting with prefix.
        ignore_file_prefix {string} -- Ignore all files starting with prefix.

    Returns: dict -- {__doc__:function callable} for each *.py file in *dir_path*.
    """

    functions = {}
    filepaths = (glob.glob('{}**/*.py'.format(dir_path)) +
                 glob.glob('{}/*.py'.format(dir_path)))

    if not filepaths:
        err = 'No .py files found in "{}"'.format(filepaths)
        logger.warning(err)
        return None

    plugin_files = []
    for filepath in filepaths:
        _, filename = os.path.split(filepath)
        if filename.startswith(include_file_prefix) and not filename.startswith(ignore_file_prefix) and not filepath in plugin_files:
            plugin_files.append(filepath)
    return plugin_files


def load_plugin_functions(filepaths, include_prefix='', ignore_prefix='_'):
    functions = {}
    docs = []
    for filepath in filepaths:
        logger.info('Checking {}'.format(filepath))
        doc, f = find_plugin_functions(filepath, include_prefix=include_prefix, ignore_prefix = ignore_prefix)
        functions.update(f)
        docs.append(doc)
    return docs, functions

