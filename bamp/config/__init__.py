import importlib
import logging
import os.path
from functools import wraps

import click

from bamp.exc import ErrorConfigParsing, MissingConfigParser

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    'vcs': 'git',
    'commit': False,
    'message': 'Bamp version: {current_version} -> {new_version}',
    'tag_name': '{new_version}',
    'tag': False,
    'files': [],
    'allow_dirty': False
}


def add_config(func):
    """Decorator for adding config file to bamp list

    In order to keep the latest version in the config file.
    The config file must be added automatically to list of bamped files,
    if it exists of course.

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        conf = find_config()
        files = kwargs.get('files')
        if files and conf and conf not in files:
            kwargs['files'] += (conf, )
        return func(*args, **kwargs)

    return wrapper


def find_config():
    """Locate config file

    TODO: Should this function be defined in config plugin file?
    TODO: Would it be better to have an object of config, it would mean the
          state could be kept during whole execution. Is it really needed?

    :returns: config filename or None

    """
    ctx = click.get_current_context()
    if ctx.params.get('config'):
        return ctx.params.get('config')
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
    # TODO: convert 'bools' into bools
    def_copy = DEFAULT_CONFIG.copy()
    def_copy.update(config)
    return def_copy


def get_config_module(filename):
    """Retrieve module responsible for parsing specific config file format.

    :param filename: name of file with configuration
    :type filename: str
    :returns: module loaded based on config file format
    :rtype: module
    :raises: MissingConfigParser

    """
    _, ext = os.path.splitext(filename)
    if ext == '.cfg':  # this really is INI
        ext = '.ini'  # would some mapping be better?

    try:
        with open(filename) as f:
            if 'bumpversion' in f.read():
                ext = '.bumpversion'
    except IOError:
        pass

    try:
        conf_module = importlib.import_module(__name__ + ext)
    except ImportError:
        raise MissingConfigParser()
    return conf_module


def prepare_config(filename):
    """Translate config file into config dictionary.

    Add configuration file so the version stored in it can be bamped.
    Function calls specific config parsing function based on config file
    format.

    :param filename: name of file with configuration
    :type filename: str
    :returns: modified config dictionary
    :rtype: dict
    :raises: ErrorConfigParsing

    """
    config = get_config_module(filename)
    try:
        conf_dict = config.prepare_config(filename)
    except ErrorConfigParsing:
        logger.exception('Error parsing config.')
        raise
    return conf_dict


def get_root_path():
    """TODO"""
    conf = find_config()
    root_path = os.path.abspath(os.path.curdir)
    if conf:
        root_path, _ = os.path.split(os.path.abspath(conf))
    return root_path
