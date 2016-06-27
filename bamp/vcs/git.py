from dulwich.repo import Repo


def get_repo(repo_path):
    return Repo(repo_path)


def create_commit(files, message):
    pass


def create_tag(commit, tag):
    pass
