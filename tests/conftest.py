from tempfile import mkdtemp

import pytest
from dulwich import porcelain


@pytest.fixture(scope='session')
def git_repo(path=None):
    """Fixture creating git repo.
    Can be used as a pytest fixture, in such case path where repo is created
    is random, created using tempfile module.
    If used as a function can be provided with path where the repo will be
    created

    :param path: path where repo will be created
    :type path: string
    :returns: porcelain object

    """
    if not path:
        path = mkdtemp()
    repo = porcelain.init(path)
    config = repo.get_config()
    config.set(b'user', b'name', b'Mr. Git')
    config.set(b'user', b'email', b'mr.git@dulwich.co.uk')
    config.write_to_path()
    return repo
