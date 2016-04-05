import os.path
import importlib


def get_config(filename):
    """Load config module base on the config file format

    Loading of config module is based on extension of the file.
    If there is no extension INI style is assumed.

    :param filename: name of the config file
    :type filename: str
    :returns: configuration loaded from file

    """
    root, ext = os.path.splitext(filename)
    if ext == '.cfg':  # this really is INI
        ext = '.ini'  # would some mapping be better?
    conf_module = importlib.import_module(__name__ + ext)
    return conf_module.load_config()
