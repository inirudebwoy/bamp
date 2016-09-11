# -*- coding: utf-8 -*-
import os
from tempfile import mkstemp, mkdtemp

import pytest
from dulwich import porcelain

from bamp.exc import VCSException
from bamp.vcs.git import is_tree_clean, get_repo, create_commit


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


@pytest.fixture
def git_repo():
    path = mkdtemp()
    repo = porcelain.init(path)
    config = repo.get_config()
    config.set('user', 'name', 'Mr. Git')
    return repo


def test_create_commit_with_unicode_message(git_repo):
    commit_sha1 = create_commit(git_repo, '', u'bździągwą')
    assert commit_sha1


def test_create_commit_with_message(git_repo):
    commit_sha1 = create_commit(git_repo, '', 'a')
    assert commit_sha1
