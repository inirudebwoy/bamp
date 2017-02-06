"""
Module supporting INI type config files.

"""
import logging

from bamp.exc import ErrorConfigParsing
from six.moves import configparser

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
    'files' key in the config object can be have a multiline value. It is
    converted into a tuple by slicing on the '\n' char. Single line 'files'
    value is converted into single element tuple.

    :param config: config to convert
    :type config: ConfigParser
    :returns: config in form of dictionary
    :rtype: dict

    """
    dict_config = {}
    bamp_sections = [s for s in config.sections() if 'bamp' in s]
    for section in bamp_sections:
        for key_item, value_item in config.items(section):
            # transforming files variable into tuple
            if key_item == 'files' and '\n' in value_item:  # multiline
                value_item = tuple(value_item.split())
            elif key_item == 'files':
                value_item = (value_item, )
            dict_config[key_item] = value_item
    return dict_config


def prepare_config(filename):
    """Parse config and create ConfigParser object.

    :param filename: Name of the config file
    :type filename: str
    :returns: Parsed config
    :rtype: ConfigParser
    :raises: ErrorParsingConfig

    """
    try:
        config = load_config(filename)
    except configparser.Error:
        logger.exception('Config could not be parsed due to an error.')
        raise ErrorConfigParsing()
    return config
