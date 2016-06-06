import os.path
import importlib

from bamp.exc import MissingConfigParser


def get_config_path():
    """ Find config file path

    Function searches for "bamp.cfg" file within project directory or "setup.cfg"

    """

    return '.setup.cfg'


def parse_config(config_path):
    pass


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
        raise MissingConfigParser()
    return conf_module.load_config()
