import os
from tempfile import mkstemp

import pytest
from dulwich import porcelain

from bamp.exc import VCSException
from bamp.vcs.git import is_tree_clean, get_repo


class RepoStatusMock(object):
    def __init__(self, staged, unstaged):
        self.unstaged = unstaged
        self.staged = staged


def status_mockreturn(mock_status):
    return RepoStatusMock(**mock_status)


def test_is_tree_clean_no_staged_no_unstaged(monkeypatch):
    monkeypatch.setattr(porcelain, 'status', status_mockreturn)
    assert is_tree_clean({'staged': {}, 'unstaged': []})


def test_is_tree_clean_no_staged_with_unstaged(monkeypatch):
    monkeypatch.setattr(porcelain, 'status', status_mockreturn)
    assert not is_tree_clean({'staged': {}, 'unstaged': ['file']})


def test_is_tree_clean_with_staged_no_unstaged(monkeypatch):
    monkeypatch.setattr(porcelain, 'status', status_mockreturn)
    assert not is_tree_clean({'staged': {'file': 'path'}, 'unstaged': []})


def test_is_tree_clean_with_staged_with_unstaged(monkeypatch):
    monkeypatch.setattr(porcelain, 'status', status_mockreturn)
    assert not is_tree_clean({'staged': {'file': 'path'},
                              'unstaged': ['moar files']})


def test_get_repo_raise_exception():
    _, path = mkstemp()
    with pytest.raises(VCSException):
        get_repo(path)

    # cleanup
    os.remove(path)
