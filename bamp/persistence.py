import logging
import os
import re
from collections import namedtuple
from io import open
from shutil import copy, copystat
from tempfile import mkstemp

from bamp.exc import VersionNotFound
from bamp.helpers.ui import verify_response

PathPair = namedtuple("PathPair", ["orig", "copy"])

logger = logging.getLogger(__name__)


@verify_response
def bamp_files(cur_version, new_version, files, limit=1):
    """Replace current version with new version in every file from list
    of files.
    If there is a problem with accessing any one of the files, operation is
    aborted and no changes are saved.

    :param cur_version: current version
    :type cur_version: str
    :param new_version: new version, replacing current
    :type new_version: str
    :param files: list of paths which to bamp
    :type files: list
    :param limit: how many times to replace version in file (default 1)
    :type limit: int
    :returns: True, [] if env is sane, False and list of error message
              otherwise
    :rtype: tuple(bool, list(str))

    """
    bamped_files = []
    errors = []
    try:
        for f in files:
            try:
                bamped_files.append(_file_bamper(cur_version, new_version, f, limit))
            except IOError:
                errors.append("Error accessing file: {0}".format(f))
            except VersionNotFound:
                errors.append("Version {0} not found in {1}".format(cur_version, f))

        if errors:
            return False, errors

        for orig, bamped in bamped_files:
            copy(bamped, orig)

        return True, []
    finally:
        # clear temps
        _rm_files([p.copy for p in bamped_files])


def _rm_files(file_list):
    """Remove files passed in a list

    :param file_list: list of paths
    :type file_list: list

    """
    for f in file_list:
        os.remove(f)


def _ver_is_found(version, line):
    # only version number is in line
    if version == line:
        return True

    ver_re = '(?<=[" \'=:v]){}[" \\\r\\n]*'.format(version)
    return bool(re.search(ver_re, line))


def _file_bamper(cur_version, new_version, file_path, limit=1):
    """Replace version in file

    Function works on a copy of a original file and returns
    namedtuple storing both versions of file.
    If the file doesn't contain the current version info is printed
    for the user.

    :param cur_version: current version
    :type cur_version: str
    :param new_version: new bamped version
    :type new_version: str
    :param file_path: path to file with current version
    :type file_path: str
    :param limit: how many times to replace version in file (default 1)
    :type limit: int
    :returns: tuple with original file and bamped copy
    :rtype: PathPair namedtuple

    """
    _, copy_path = mkstemp()
    with open(copy_path, mode="w", encoding="utf-8") as cf:
        with open(file_path, encoding="utf-8") as of:
            found = 0
            for line in of.readlines():
                if _ver_is_found(cur_version, line):
                    if found < limit or limit == 0:
                        line = line.replace(cur_version, new_version)
                    found += 1
                cf.write(line)
            if not found:
                raise VersionNotFound()
            copystat(file_path, copy_path)

    return PathPair(file_path, copy_path)
