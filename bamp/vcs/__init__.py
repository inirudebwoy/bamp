"""
Module providing support for pluggable VCS support

TODO: should I provide interface for VCS plugins?
"""

import logging
import importlib

from bamp.exc import MissingVcsModule


logger = logging.getLogger(__name__)


def _get_vcs_module(vcs_type):
    """Load VCS module according to type passed

    :param vcs_type: name of plugin to load, 'git' or 'hg'
    :type vcs_type: str
    :returns: module

    """
    try:
        vcs_module = importlib.import_module(
            '{0}.{1}'.format(__name__, vcs_type))
    except ImportError:
        raise MissingVcsModule()
    return vcs_module


def create_commit(vcs_type, files, message):
    """Create a commit

    Function creates a commit with specified message and chosen list of
    files.

    :param vcs_type: name of vcs to be used
    :type vcs_type: str
    :param files: list of files to add to commit
    :type files: list
    :param message: commit message
    :type message: str

    """
    vcs = _get_vcs_module(vcs_type)
    repo = vcs.get_repo('.')
    return vcs.create_commit(repo, files, message)


def is_tree_clean(vcs_type, repo_path):
    """Verify if repository is clean

    :param vcs_type: name of vcs to be used
    :type vcs_type: str
    :param repo_path: path to the vcs repository dir
    :type repo_path: str
    :returns: True, '' if tree is clean, False and error message otherwise
    :rtype: tuple(bool, str)

    """
    vcs = _get_vcs_module(vcs_type)
    clean = vcs.is_tree_clean(repo_path)
    if not clean:
        return False, 'Directory is not clean. Commit or stash your changes.'
    return True, ''


def make_message(message, current_version, new_version):
    """Create a commit message

    :param message: commit message format
    :type message: str
    :param current_version: current version
    :type current_version: str
    :param new_version: new bamp version
    :type new_version: str
    :returns: commit message
    :rtype: str
    """
    return message.format(current_version=current_version,
                          new_version=new_version)
