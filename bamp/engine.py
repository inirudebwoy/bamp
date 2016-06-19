"""
TODO: create new option type to make sure that it is in correct format?
      this would move validation off the functions into the interface, where
      it should be.

TODO: meta and pre-releases

"""
from shutil import copy2
from io import open
from tempfile import mkstemp
import logging
from collections import OrderedDict

from .exc import IncorrectPart
from .config import find_config

# TODO: taken from config
VERSION_PARTS = ('major', 'minor', 'patch')
VERSION_SEPARATOR = '.'

logger = logging.getLogger(__name__)
logging.basicConfig()


def split_version(version):
    """Split incoming version into namedtuple

    :param version: version in form of comma separated string
    :type version: str
    :returns: version in form of namedtuple (keys: ('major', 'minor', 'patch'))
    :rtype: namedtuple SplitVersion

    """
    int_list = map(int, version.split(VERSION_SEPARATOR))
    return OrderedDict(zip(VERSION_PARTS, int_list))


def join_version(version_list):
    """Join version in form namedtuple into string

    :param version_list: version elements
    :type version_list: iterable
    :returns: version as string, comma separated
    :rtype: str

    """
    str_list = map(str, version_list)
    return VERSION_SEPARATOR.join(str_list)


def _bamp(version, part):
    """Bump version according to semantic versioning

    :param version: version to bump
    :type version: iterable
    :param part: name of the part to be bumped
    :type part: str
    :returns: bumped version
    :rtype: namedtuple SplitVersion

    """
    new_values = []
    zero_rest = False
    for i, v in version.items():
        if zero_rest:
            new_values.append(0)
            continue

        if i == part:
            new_values.append(v + 1)
            zero_rest = True
        else:
            new_values.append(v)
    return OrderedDict(zip(VERSION_PARTS, new_values))


def bamp_version(version, part, files):
    # TODO: checkes done here
    version = split_version(version)
    if part not in version:
        raise IncorrectPart(
            '{0} could not be found in {1}'.format(part, version))

    bamped = _bamp(version, part)
    return join_version(bamped.values())


def bamp_files(cur_version, new_version, files):
    # bamp the config if present
    config = find_config()
    if config:
        files += (config, )

    bamped_files = [_file_bamper(cur_version, new_version, f) for f in files]
    for orig, bamped in bamped_files:
        copy2(bamped, orig)


def _file_bamper(cur_version, new_version, file_path):
    # make a copy
    _, copy_path = mkstemp()
    # bamp copy
    with open(copy_path, mode='w', encoding='utf-8') as cf:
        with open(file_path, encoding='utf-8') as of:
            for line in of.readlines():
                if cur_version in line:
                    line = line.replace(cur_version, new_version)
                cf.write(line)

    return (file_path, copy_path)
