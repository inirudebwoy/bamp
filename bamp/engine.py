"""
TODO: create new option type to make sure that it is in correct format?
      this would move validation off the functions into the interface, where
      it should be.

TODO: meta and pre-releases

"""
from collections import namedtuple

VERSION_PARTS = ('major', 'minor', 'patch')
SplitVersion = namedtuple('SplitVersion', VERSION_PARTS)

VERSION_SEPARATOR = '.'


def split_version(version):
    int_list = map(int, version.split(VERSION_SEPARATOR))
    return SplitVersion(*int_list)


def join_version(version_list):
    str_list = map(str, version_list)
    return VERSION_SEPARATOR.join(str_list)


def bamp_version(version, part):
    try:
        current_value = getattr(version, part)
    except AttributeError:
        # TODO: raise own exception?
        return None

    return version._replace(**{part: current_value + 1})
