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


def repo(repo_path, vcs_type):
    vcs = _get_vcs_module(vcs_type)
    return vcs.get_repo(repo_path)


def create_commit(vcs_type, files, message):
    vcs = _get_vcs_module(vcs_type)
    return vcs.create_commit(files, message)
