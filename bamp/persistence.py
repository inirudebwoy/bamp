import logging
import os
from shutil import copy2
from io import open
from tempfile import mkstemp
from collections import namedtuple


PathPair = namedtuple('PathPair', ['orig', 'copy'])

logger = logging.getLogger(__name__)


def bamp_files(cur_version, new_version, files):
    """Replace current version with new version in every file from list
    of files.
    If there is a problem with accessing any one of the files, operation is
    aborted and no changes are saved.

    TODO: update
    :param cur_version: current version
    :type cur_version: str
    :param new_version: new version, replacing current
    :type new_version: str
    :param files: list of paths which to bamp
    :type files: list
    :returns:
    :rtype: tuple

    """
    bamped_files = []
    errors = []
    for f in files:
        try:
            bamped_files.append(_file_bamper(cur_version, new_version, f))
        except IOError:
            logger.exception('Error accessing file: %s', f)
            logger.error('Bamping cancelled.')
            errors.append('Error accessing file: %s'.format(f))

    if errors:
        return False, errors

    for orig, bamped in bamped_files:
        copy2(bamped, orig)

    # clear temps
    _rm_files([p.copy for p in bamped_files])
    return True, []


def _rm_files(file_list):
    """Remove files passed in a list

    :param file_list: list of paths
    :type file_list: list

    """
    for f in file_list:
        os.remove(f)


def _file_bamper(cur_version, new_version, file_path):
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
    :returns: tuple with original file and bamped copy
    :rtype: PathPair namedtuple

    """
    _, copy_path = mkstemp()
    with open(copy_path, mode='w', encoding='utf-8') as cf:
        with open(file_path, encoding='utf-8') as of:
            found = False
            for line in of.readlines():
                if cur_version in line:
                    found = True
                    line = line.replace(cur_version, new_version)
                cf.write(line)
            if not found:
                logger.info(
                    "Couldn't find current version '%s' in file: %s",
                    cur_version, of.name)

    return PathPair(file_path, copy_path)
