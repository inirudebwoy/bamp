from collections import OrderedDict

import pytest

from bamp.engine import (split_version, join_version, _bamp,
                         bamp_version)
from bamp.exc import IncorrectPart


def test_split_simple():
    result = split_version('0.0.1')
    assert result.get('major') == 0
    assert result.get('minor') == 0
    assert result.get('patch') == 1


def test_split_complex():
    result = split_version('1.30.1')
    assert result.get('major') == 1
    assert result.get('minor') == 30
    assert result.get('patch') == 1


def test_join():
    assert join_version([0, 0, 1]) == '0.0.1'


def make_version(values):
    return OrderedDict(zip(('major', 'minor', 'patch'), values))


def test_bamp_patch():
    assert _bamp(make_version((0, 0, 1)), 'patch') == make_version((0, 0, 2))


def test_bamp_patch_with_major_minor():
    assert _bamp(make_version((2, 3, 4)), 'patch') == make_version((2, 3, 5))


def test_bamp_minor():
    assert _bamp(make_version((0, 0, 9)), 'minor') == make_version((0, 1, 0))


def test_bamp_minor_with_patch_major():
    assert _bamp(make_version((2, 8, 10)), 'minor') == make_version((2, 9, 0))


def test_bamp_major_with_minor():
    assert _bamp(make_version((0, 1, 1)), 'major') == make_version((1, 0, 0))


def test_bamp_major():
    assert _bamp(make_version((2, 0, 1)), 'major') == make_version((3, 0, 0))


def test_bamp_version():
    assert bamp_version('0.0.1', 'patch') == '0.0.2'


def test_bamp_version_bad_part():
    with pytest.raises(IncorrectPart):
        bamp_version('0.0.1', 'foobar')
