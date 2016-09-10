import pytest

from bamp.vcs import _get_vcs_module
from bamp.exc import MissingVcsModule


def test_get_vcs_module_git():
    vcs = _get_vcs_module('git')
    assert vcs.__name__ == 'bamp.vcs.git'


def test_get_vcs_module_failed():
    with pytest.raises(MissingVcsModule):
        _get_vcs_module('Albatros')
