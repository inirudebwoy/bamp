from collections import namedtuple

from bamp.engine import split_version, join_version, bamp_version

SplitVersion = namedtuple('SplitVersion', ['major', 'minor', 'patch'])


def test_split():
    result = split_version('0.0.1')
    assert result.major == 0
    assert result.minor == 0
    assert result.patch == 1


def test_join():
    assert join_version([0, 0, 1]) == '0.0.1'


def test_bamp_version():
    assert bamp_version(SplitVersion(0, 0, 1), 'part') == SplitVersion(0, 0, 2)
