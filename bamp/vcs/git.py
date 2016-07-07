"""
Module supporting Git vcs

"""

from dulwich import porcelain
from dulwich.repo import NotGitRepository


def repo_exists(repo_path):
    """Check if repo exists

    :param repo_path: path to the repo
    :type repo_path: str
    :returns: True if exists, False otherwise
    :rtype: bool

    """
    try:
        get_repo(repo_path)
    except NotGitRepository:
        return False
    return True


def get_repo(repo_path):
    """Retrieve repository

    :param repo_path: path to .git directory
    :type repo_path: str
    :returns: loaded repository
    :rtype: dulwich.Repo

    """
    return porcelain.open_repo(repo_path)


def is_tree_clean(repo):
    """Check if git status is clean

    Unstaged changes or staged will return False.

    :param repo: repository
    :type repo: dulwich.Repo

    """
    status = porcelain.status(repo)
    return not (status.unstaged or any(status.staged.values()))


def create_commit(repo, files, message):
    """Create a commit

    :param repo: git repository
    :type repo: dulwich.Repo
    :param files: list of files to be added to commit
    :type files: list
    :param message: commit message
    :type: str

    """
    for f in files:
        porcelain.add(repo, f)
    porcelain.commit(repo, message)
