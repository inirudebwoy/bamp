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
    """Bumpversion supports file or part specific config. It is achieved by
    formatting name of the section in certain way.

    [bumpversion:file:./path.py]

    Function at this point supports only parsing the paths in file specific
    section and appends them to bamp config file section.
    Other configuration included in specific section is not supported yet.

    """
    dict_config = {}
    bumpversion_sections = [s for s in config.sections() if 'bumpversion' in s]

    for section in bumpversion_sections:
        if ':' not in section:
            for key_item, value_item in config.items(section):

                # bumpversion uses current_version instead of version
                if key_item == 'current_version':
                    key_item = 'version'

                dict_config[key_item] = value_item
        else:
            sub = section.split(':')[2]
            files = dict_config.get('files', ())
            dict_config['files'] = files + (sub, )

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
