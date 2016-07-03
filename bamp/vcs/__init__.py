import logging
import importlib

from bamp.exc import MissingVcsModule


logger = logging.getLogger(__name__)


def _get_vcs_module(vcs_type):
    try:
        vcs_module = importlib.import_module(
            '{0}.{1}'.format(__name__, vcs_type))
    except ImportError:
        raise MissingVcsModule()
    return vcs_module


def create_commit(vcs_type, files, message):
    vcs = _get_vcs_module(vcs_type)
    repo = vcs.get_repo('.')
    return vcs.create_commit(repo, files, message)


def is_tree_clean(vcs_type, repo_path):
    vcs = _get_vcs_module(vcs_type)
    clean = vcs.is_tree_clean(repo_path)
    if not clean:
        return False, 'Directory is not clean. Commit or stash your changes.'
    return True, ''


def make_message(message, current_version, new_version):
    return message.format(current_version=current_version,
                          new_version=new_version)
