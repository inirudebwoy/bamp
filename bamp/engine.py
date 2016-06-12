"""
TODO: create new option type to make sure that it is in correct format?
      this would move validation off the functions into the interface, where
      it should be.

TODO: meta and pre-releases

"""
from collections import OrderedDict

from .exc import IncorrectPart

# TODO: taken from config
VERSION_PARTS = ('major', 'minor', 'patch')
VERSION_SEPARATOR = '.'


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


def part_in_version(version, part):
    return part in version


def bamp_version(version, part, config):
    version = split_version(version)
    if part_in_version(version, part):
        bamped = _bamp(version, part)
        return join_version(bamped.values())
    raise IncorrectPart('{0} could not be found in {1}'.format(part, version))
