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
    """

    Bumpversion supports file or part specific config. It is achieved by
    formatting name of the section in certain way.

    [bumpversion:file:./path.py]

    Function at this point supports only parsing the paths in file specific
    section and appends them to bamp config file section.
    Other configuration included in specific section is not supported yet.

    """
    dict_config = {}
    bumpversion_sections = [s for s in config.sections()
                            if 'bumpversion' in s]

    for section in bumpversion_sections():
        dict_item = {}
        # identify if it's a files section
        # extract filepath
        # create files section
        # add filepath to files section
        try:
            _, main, sub = section.split(':')
        except ValueError:
            key_item = 'files'
            value_item = sub

        for key_item, value_item in config.items(section):
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
    try:
        config = load_config(filename)
    except configparser.Error:
        logger.exception('Config could not be parsed due to an error.')
        raise ErrorConfigParsing()
    return config
