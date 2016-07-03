from dulwich import porcelain


def get_repo(repo_path):
    return porcelain.open_repo(repo_path)


def is_tree_clean(repo):
    status = porcelain.status(repo)
    return not (status.unstaged or any(status.staged.values()))


def create_commit(repo, files, message):
    for f in files:
        porcelain.add(repo, f)
    porcelain.commit(repo, message)
