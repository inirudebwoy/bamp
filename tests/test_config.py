import pytest

from bamp.config import DEFAULT_CONFIG, make_default_map, get_config_module
from bamp.exc import MissingConfigParser


def test_empty_config():
    assert make_default_map({}) == DEFAULT_CONFIG


def test_empty_bamp_section():
    assert make_default_map({'bamp': {}}) == DEFAULT_CONFIG


def test_override_default_value():
    def_map = make_default_map({'bamp': {'tag': True}})
    assert def_map.get('tag')


def test_override_all_values():
    config = {'bamp': {'vcs': 'other',
                       'commit': True,
                       'message': 'Larch',
                       'tag': True,
                       'files': 'yes',
                       'allow_dirty': True}}
    def_map = make_default_map(config)
    for k in def_map:
        assert def_map.get(k) == config.get('bamp').get(k)


def test_get_config_module_cfg_ext():
    module = get_config_module('setup.cfg')
    assert 'ini' in module.__name__


def test_get_config_module_ini_ext():
    module = get_config_module('setup.ini')
    assert 'ini' in module.__name__


def test_get_config_module_unknown_ext():
    with pytest.raises(MissingConfigParser):
        get_config_module('setup.unknown')
