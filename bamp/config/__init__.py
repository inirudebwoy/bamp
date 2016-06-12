import os.path
import importlib

from bamp.exc import MissingConfigParser


def find_config():
    """TODO

    config lookup"""
    if os.path.exists('bamp.cfg'):
        return 'bamp.cfg'
    elif os.path.exists('setup.cfg'):
        return 'setup.cfg'
    else:
        return None


def parse_config(filename, input_args):
    """TODO

    merging config with input_params
    """
    # TODO: this should throw exception when config is malformed
    config = get_config(filename)
    return config


def get_config(filename):
    """Load config module base on the config file format

    Loading of config module is based on extension of the file.
    If there is no extension INI style is assumed.

    :param filename: name of the config file
    :type filename: str
    :raises: MissingConfigParser
    :returns: configuration loaded from file

    """
    root, ext = os.path.splitext(filename)
    if ext == '.cfg':  # this really is INI
        ext = '.ini'  # would some mapping be better?
    try:
        conf_module = importlib.import_module(__name__ + ext)
    except ImportError:
        raise MissingConfigParser
    return conf_module.load_config(filename)
