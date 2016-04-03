import pytest

from bamp.engine import split_version, join_version, _bamp, SplitVersion, \
    bamp_version
from bamp.exc import IncorrectPart


def test_split_simple():
    result = split_version('0.0.1')
    assert result.major == 0
    assert result.minor == 0
    assert result.patch == 1


def test_split_complex():
    result = split_version('1.30.1')
    assert result.major == 1
    assert result.minor == 30
    assert result.patch == 1


def test_join():
    assert join_version([0, 0, 1]) == '0.0.1'


def test_bamp_patch():
    assert _bamp(SplitVersion(0, 0, 1), 'patch') == SplitVersion(0, 0, 2)


def test_bamp_patch_with_major_minor():
    assert _bamp(SplitVersion(2, 3, 4), 'patch') == SplitVersion(2, 3, 5)


def test_bamp_minor():
    assert _bamp(SplitVersion(0, 0, 9), 'minor') == SplitVersion(0, 1, 0)


def test_bamp_minor_with_patch_major():
    assert _bamp(SplitVersion(2, 8, 10), 'minor') == SplitVersion(2, 9, 0)


def test_bamp_major_with_minor():
    assert _bamp(SplitVersion(0, 1, 1), 'major') == SplitVersion(1, 0, 0)


def test_bamp_major():
    assert _bamp(SplitVersion(2, 0, 1), 'major') == SplitVersion(3, 0, 0)


def test_bamp_version():
    assert bamp_version(SplitVersion(0, 0, 1), 'patch') == SplitVersion(0, 0, 2)


def test_bamp_version_bad_part():
    with pytest.raises(IncorrectPart):
        bamp_version(SplitVersion(0, 0, 1), 'foobar')
