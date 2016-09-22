import pytest

from bamp.vcs import _get_vcs_module, make_tag_name, create_tag
from bamp.exc import MissingVcsModule


def test_get_vcs_module_git():
    vcs = _get_vcs_module('git')
    assert vcs.__name__ == 'bamp.vcs.git'


def test_get_vcs_module_failed():
    with pytest.raises(MissingVcsModule):
        _get_vcs_module('Albatros')


def test_make_tag_name_no_substitution():
    tag_message = 'it\'s a tag'
    assert make_tag_name(tag_message, '0.9.0') == tag_message


def test_make_tag_name_with_substitution():
    tag_message = '{new_version}-tag'
    assert make_tag_name(tag_message, '1.1.1') == '1.1.1-tag'
