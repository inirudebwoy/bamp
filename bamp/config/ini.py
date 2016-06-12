import logging
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

logger = logging.getLogger(__name__)
logging.basicConfig()


def load_config(filename):
    """ TODO """
    parser = configparser.ConfigParser()
    parser.read(filename)
    return config_dump(parser)


def config_dump(config):
    """ TODO

    multiline into list etc.
    spit out dict"""
    dict_config = {}
    for section in config.sections():
        dict_item = {}
        for key_item, value_item in config.items(section):
            if '\n' in value_item:  # multiline
                value_item = value_item.split()
            dict_item[key_item] = value_item
        dict_config[section] = dict_item
    return dict_config
