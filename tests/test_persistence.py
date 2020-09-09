from bamp.persistence import _ver_is_found


def test_issue_15():
    assert not _ver_is_found("1.0.22", 'INTERNAL_IPS = ["127.1.0.22"]')
    assert _ver_is_found("1.0.22", 'VERSION = "1.0.22"')

def test_only_version_number_in_line():
    assert _ver_is_found("1.0.22", "1.0.22")
    assert _ver_is_found("1.0.22", "  1.0.22")
    assert _ver_is_found("1.0.22", "  1.0.22   \n")

def test_version_in_configuration():
    assert _ver_is_found("1.0.22", "version=1.0.22")
    assert _ver_is_found("1.0.22", "version=1.0.22\n")
