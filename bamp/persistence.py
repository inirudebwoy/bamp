import os
from shutil import copy2
from io import open
from tempfile import mkstemp
from collections import namedtuple


PathPair = namedtuple('PathPair', ['orig', 'copy'])


def bamp_files(cur_version, new_version, files):
    """Replace current version with new version in every file from list
    of files.

    If 

    :param cur_version: current version
    :type cur_version: str
    :param new_version: new version, replacing current
    :type new_version: str
    :param files: list of paths which to bamp
    :type files: list

    """
    bamped_files = [_file_bamper(cur_version, new_version, f) for f in files]
    for orig, bamped in bamped_files:
        copy2(bamped, orig)

    # clear temps
    _rm_files([p.copy for p in bamped_files])


def _rm_files(file_list):
    """Remove files passed in a list

    :param file_list: list of paths
    :type file_list: list

    """
    for f in file_list:
        os.remove(f)


def _file_bamper(cur_version, new_version, file_path):
    """

    :param cur_version:
    :type cur_version:
    :param new_version:
    :type new_version:
    :param file_path:
    :type file_path:
    :returns:
    :rtype: PathPair namedtuple

    """
    _, copy_path = mkstemp()
    with open(copy_path, mode='w', encoding='utf-8') as cf:
        with open(file_path, encoding='utf-8') as of:
            for line in of.readlines():
                if cur_version in line:
                    line = line.replace(cur_version, new_version)
                cf.write(line)

    return PathPair(file_path, copy_path)
