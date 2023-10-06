import os
from tempfile import NamedTemporaryFile

from bamp.persistence import _ver_is_found, _file_bamper

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
    assert _ver_is_found("1.2.3", "image = 'flyte/chuddyserver:1.2.3'")
    assert _ver_is_found("1.2.3", "image = 'flyte/chuddyserver:1.2.3'\n") 
    assert _ver_is_found("1.1.1", "version = 'v1.1.1'")
    assert _ver_is_found("1.1.1", "'v1.1.1'\n")
    assert _ver_is_found("1.1.1", " v1.1.1\n")

def test_limit_default():
    with NamedTemporaryFile("w", encoding="utf-8") as f:
        f.write("""\
first_version=1.33.7
second_version=1.33.7
third_version=1.33.7
""")
        f.flush()
        _, new_file = _file_bamper("1.33.7", "1.33.8", f.name)
        try:
            with open(new_file, "r", encoding="utf-8") as nf:
                assert nf.read() == """\
first_version=1.33.8
second_version=1.33.7
third_version=1.33.7
"""
        finally:
            os.remove(new_file)


def test_limit_2():
    with NamedTemporaryFile("w", encoding="utf-8") as f:
        f.write("""\
first_version=1.33.7
second_version=1.33.7
third_version=1.33.7
""")
        f.flush()
        _, new_file = _file_bamper("1.33.7", "1.33.8", f.name, limit=2)
        try:
            with open(new_file, "r", encoding="utf-8") as nf:
                assert nf.read() == """\
first_version=1.33.8
second_version=1.33.8
third_version=1.33.7
"""
        finally:
            os.remove(new_file)

def test_limit_0():
    with NamedTemporaryFile("w", encoding="utf-8") as f:
        f.write("""\
first_version=1.33.7
second_version=1.33.7
third_version=1.33.7
""")
        f.flush()
        _, new_file = _file_bamper("1.33.7", "1.33.8", f.name, limit=0)
        try:
            with open(new_file, "r", encoding="utf-8") as nf:
                assert nf.read() == """\
first_version=1.33.8
second_version=1.33.8
third_version=1.33.8
"""
        finally:
            os.remove(new_file)