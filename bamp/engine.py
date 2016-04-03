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
    """Split incoming version into namedtuple

    :param version: version in form of comma separated string
    :type version: str
    :returns: version in form of namedtuple (keys: ('major', 'minor', 'patch'))
    :rtype: namedtuple SplitVersion

    """
    int_list = map(int, version.split(VERSION_SEPARATOR))
    return SplitVersion(*int_list)


def join_version(version_list):
    """Join version in form namedtuple into string

    :param version_list: version elements
    :type version_list: iterable
    :returns: version as string, comma separated
    :rtype: str

    """
    str_list = map(str, version_list)
    return VERSION_SEPARATOR.join(str_list)


# TODO: this should be a private function
def bamp_version(version, part):
    """Bump version according to semantic versioning

    :param version: version to bump
    :type version: iterable
    :param part: name of the part to be bumped
    :type part: str
    :returns: bumped version
    :rtype: namedtuple SplitVersion

    """
    # TODO: will this be called from other places than UI?
    #       this validation could be moved outside
    try:
        getattr(version, part)
    except AttributeError:
        # TODO: raise own exception?
        return None

    new_values = []
    for i, v in version._asdict().items():
        if version._fields.index(i) > version._fields.index(part):
            new_values.append(0)
        elif version._fields.index(i) == version._fields.index(part):
            new_values.append(v + 1)
        else:
            new_values.append(v)

    return SplitVersion(*new_values)
