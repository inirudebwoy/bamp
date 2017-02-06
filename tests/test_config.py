import pytest

import bamp
from bamp.config import (DEFAULT_CONFIG, make_default_map, get_config_module,
                         prepare_config)
from bamp.exc import MissingConfigParser, ErrorConfigParsing


def test_empty_config():
    assert make_default_map({}) == DEFAULT_CONFIG


def test_override_default_value():
    def_map = make_default_map({'tag': True})
    assert def_map.get('tag')


def test_override_all_values():
    config = {
        'vcs': 'other',
        'commit': True,
        'message': 'Larch',
        'tag_name': 'Spam',
        'tag': True,
        'files': 'yes',
        'allow_dirty': True
    }
    def_map = make_default_map(config)
    for k in def_map:
        assert def_map.get(k) == config.get(k)


def test_get_config_module_cfg_ext():
    module = get_config_module('setup.cfg')
    assert 'ini' in module.__name__


def test_get_config_module_ini_ext():
    module = get_config_module('setup.ini')
    assert 'ini' in module.__name__


def test_get_config_module_unknown_ext():
    with pytest.raises(MissingConfigParser):
        get_config_module('setup.unknown')


class ConfigMock(object):
    def __init__(self, callable):
        self._callable = callable

    def prepare_config(self, filename):
        return self._callable(filename)


def test_prepare_config_parsing_error(monkeypatch):
    def mockreturn(filename):
        def raiser(filename):
            raise ErrorConfigParsing

        return ConfigMock(raiser)

    monkeypatch.setattr(bamp.config, 'get_config_module', mockreturn)
    with pytest.raises(ErrorConfigParsing):
        prepare_config('config.ini')
