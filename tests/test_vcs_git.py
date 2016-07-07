from bamp.vcs.git import repo_exists


def test_repo_exists():
    assert repo_exists('.') == True


def test_repo_not_exists():
    assert repo_exists('.') == False
