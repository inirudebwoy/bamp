"""
Module supporting Git vcs

"""
import logging
from dulwich import porcelain
from dulwich.repo import NotGitRepository

from bamp.exc import VCSException

logger = logging.getLogger(__name__)


def get_repo(repo_path):
    """Retrieve repository

    :param repo_path: path to .git directory
    :type repo_path: str
    :returns: loaded repository
    :rtype: dulwich.Repo

    """
    try:
        return porcelain.open_repo(repo_path)
    except NotGitRepository:
        logger.exception('Unable to open repository.')
        raise VCSException()


def is_tree_clean(repo):
    """Check if git status is clean

    Unstaged changes or staged will return False.

    :param repo: repository
    :type repo: dulwich.Repo

    """
    status = porcelain.status(repo)
    return not (status.unstaged or any(status.staged.values()))


def create_commit(repo_path, files, message):
    """Create a commit

    :param repo_path: path to git repo
    :type repo_path: str
    :param files: list of files to be added to commit
    :type files: list
    :param message: commit message
    :type: str

    """
    repo = get_repo(repo_path)
    for f in files:
        porcelain.add(repo, f)
    porcelain.commit(repo, message)
