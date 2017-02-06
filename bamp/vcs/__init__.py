"""
Module providing support for pluggable VCS support

"""

import importlib
import logging

import click

from bamp.config import get_root_path
from bamp.exc import MissingVcsModule, VCSException
from bamp.helpers.ui import error_exit, verify_response

logger = logging.getLogger(__name__)


def _get_vcs_module(vcs_type):
    """Load VCS module according to type passed

    :param vcs_type: name of plugin to load, 'git' or 'hg'
    :type vcs_type: str
    :returns: module

    """
    try:
        vcs_module = importlib.import_module('{0}.{1}'.format(__name__,
                                                              vcs_type))
    except ImportError:
        logger.exception('Unable to find module supporting "%s".', vcs_type)
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
    root_path = get_root_path()
    vcs = _get_vcs_module(vcs_type)
    try:
        repo = vcs.get_repo(root_path)
    except VCSException as e:
        error_exit(e.args)
    try:
        return vcs.create_commit(repo, files, message)
    except:
        logger.exception('Could not create a commit message "%s" '
                         'for the repo "%s" under path "%s"', message,
                         vcs_type, root_path)
        error_exit('Could not create a commit message.')


def create_tag(vcs_type, commit_sha1, tag_name):
    # TODO: factor this out
    root_path = get_root_path()
    vcs = _get_vcs_module(vcs_type)
    try:
        repo = vcs.get_repo(root_path)
    except VCSException as e:
        error_exit(e.args)
    # this bit

    return vcs.create_tag(repo, commit_sha1, tag_name)


def make_tag_name(tag_message, new_version):
    """ TODO"""
    return tag_message.format(new_version=new_version)


@verify_response
def is_tree_clean(vcs_type, repo_path):
    """Verify if repository is clean

    :param vcs_type: name of vcs to be used
    :type vcs_type: str
    :param repo_path: path to the vcs repository dir
    :type repo_path: str
    :returns: True, '' if tree is clean, False and error message otherwise
    :rtype: tuple(bool, str)

    """
    ctx = click.get_current_context()
    if not ctx.params.get('allow_dirty'):
        return True, []

    vcs = _get_vcs_module(vcs_type)
    clean = vcs.is_tree_clean(repo_path)
    if not clean:
        return False, ['Directory is not clean. Commit or stash your changes.']
    return True, []


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
    return message.format(
        current_version=current_version, new_version=new_version)
