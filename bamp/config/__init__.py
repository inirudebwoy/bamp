import logging
import os.path
import importlib

from bamp.exc import MissingConfigParser

logger = logging.getLogger(__name__)
logging.basicConfig()


def find_config():
    """Locate config file

    :returns: config filename or None

    """
    if os.path.exists('bamp.cfg'):
        return 'bamp.cfg'
    elif os.path.exists('setup.cfg'):
        return 'setup.cfg'
    else:
        return None


def make_default_map(config):
    """Create a dictionary for default_map argument of click Command

    :param config: config object as dictionary
    :type config: dict
    :returns: dictionary with values accepted as default_map
    :rtype: dict

    """
    return config.get('bamp', {})


def get_config(filename):
    """Load config module base on the config file format

    Loading of config module is based on extension of the file.
    If there is no extension INI style is assumed.

    :param filename: name of the config file
    :type filename: str
    :raises: MissingConfigParser
    :returns: configuration loaded from file

    """
    conf_module = get_config_module(filename)
    return conf_module.load_config(filename)


def get_config_module(filename):
    root, ext = os.path.splitext(filename)
    if ext == '.cfg':  # this really is INI
        ext = '.ini'  # would some mapping be better?
    try:
        conf_module = importlib.import_module(__name__ + ext)
    except ImportError:
        raise MissingConfigParser
    return conf_module


def prepare_config(filename):
    config = get_config_module(filename)
    conf_dict = config.prepare_config(filename)
    main_section = conf_dict.get('bamp', {})
    if main_section:
        files = main_section.get('files', [])
        files.append(filename)
    return conf_dict
