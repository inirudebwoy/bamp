from bamp.engine import split_version, join_version, bamp_version, SplitVersion


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
    assert bamp_version(SplitVersion(0, 0, 1), 'patch') == SplitVersion(0, 0, 2)


def test_bamp_minor():
    assert bamp_version(SplitVersion(0, 0, 9), 'minor') == SplitVersion(0, 1, 0)


def test_bamp_major_with_minor():
    assert bamp_version(SplitVersion(0, 1, 1), 'major') == SplitVersion(1, 0, 0)


def test_bamp_major():
    assert bamp_version(SplitVersion(2, 0, 1), 'major') == SplitVersion(3, 0, 0)
