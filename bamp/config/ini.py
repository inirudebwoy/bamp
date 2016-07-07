"""
Module supporting INI type config files.

"""
import logging
from six.moves import configparser

from bamp.exc import ErrorConfigParsing

logger = logging.getLogger(__name__)


def load_config(filepath):
    """Load file under given path and return config object.

    :param filepath: path to config file
    :type filepath: str
    :returns: loaded config file
    :rtype: ConfigParser

    """
    parser = configparser.ConfigParser()
    parser.read(filepath)
    return config_dump(parser)


def config_dump(config):
    """Convert configparser object into a dictionary.
    Multiline values are converted into lists, they are sliced
    on '\n' char.

    :param config: config to convert
    :type config: ConfigParser
    :returns: config in form of dictionary
    :rtype: dict

    """
    dict_config = {}
    for section in config.sections():
        dict_item = {}
        for key_item, value_item in config.items(section):
            if '\n' in value_item:  # multiline
                value_item = value_item.split()
            dict_item[key_item] = value_item
        dict_config[section] = dict_item
    return dict_config


def prepare_config(filename):
    """Parse config and create ConfigParser object.

    :param filename: Name of the config file
    :type filename: str
    :returns: Parsed config
    :rtype: ConfigParser
    :raises: ErrorParsingConfig

    """
    if not filename:
        return {}

    try:
        config = load_config(filename)
    except configparser.Error:
        logger.exception('Config could not be parsed due to an error.')
        raise ErrorConfigParsing()
    return config
