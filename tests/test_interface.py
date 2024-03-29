from click.testing import CliRunner

from bamp.main import bamp
from .conftest import git_repo_fixture


def test_arg_part_missing():
    """bamp"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(bamp)
        assert result.exit_code == 2
        assert "Missing argument '[patch|minor|major|current]'" in result.output


def test_arg_part_no_version():
    """bamp patch"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(bamp, ["patch"])
        assert result.exit_code == 2
        assert '"version" is required.' in result.output


def test_arg_part_with_version():
    """bamp patch -v 0.0.1"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(bamp, ["patch", "-v", "0.0.1"])
        assert result.exit_code == 0


def test_arg_part_with_version_with_nonexisting_file():
    """bamp patch -v 0.0.1 -f version.ini"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(bamp, ["patch", "-v", "0.0.1", "-f", "version.ini"])
        assert result.exit_code == 2
        assert "'version.ini' does not exist" in result.output


def test_arg_part_with_version_with_existing_file():
    """bamp patch -v 0.0.1 -f version.ini"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("version.ini", "w") as v:
            v.write("0.0.1")
        result = runner.invoke(bamp, ["patch", "-v", "0.0.1", "-f", "version.ini"])

        assert result.exit_code == 0


def test_arg_unsupported_part():
    """bamp foobar"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(bamp, ["foobar"])
        assert result.exit_code == 2
        assert "Invalid value for '[patch|minor|major|current]'" in result.output


def test_with_default_commit_no_vcs():
    """bamp patch -v 3.8 -f version.ini -c"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("version.ini", "w") as v:
            v.write("image = python:3.8")
        result = runner.invoke(
            bamp, ["patch", "-v", "3.8", "-f", "version.ini", "-c"]
        )
        assert result.exit_code == 1


def test_default_tag_default_commit_with_vcs():
    """bamp patch -v v0.0.1 -f version.ini -ct"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        git_repo_fixture(".")
        with open("version.ini", "w") as v:
            v.write("v0.0.1")
        result = runner.invoke(
            bamp, ["patch", "-v", "0.0.1", "-f", "version.ini", "-c", "-t"]
        )
        assert result.exit_code == 0


def test_custom_tag_default_commit_with_vcs():
    """bamp patch -v 0.0.1 -f version.ini -c -t -T tag-{new_version}"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        git_repo_fixture(".")
        with open("version.ini", "w") as v:
            v.write("0.0.1")
        result = runner.invoke(
            bamp,
            [
                "patch",
                "-v",
                "0.0.1",
                "-f",
                "version.ini",
                "-c",
                "-t",
                "-T",
                "tag-{new_version}",
            ],
        )
        assert result.exit_code == 0

def test_limit_default():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("version.ini", "w", encoding="utf-8") as v:
            v.write("""\
first_version=1.33.7
second_version=1.33.7
third_version=1.33.7
""")
        result = runner.invoke(bamp, ["patch", "-v", "1.33.7", "-f", "version.ini"])
        assert result.exit_code == 0
        with open("version.ini", "r", encoding="utf-8") as v:
            assert v.read() == """\
first_version=1.33.8
second_version=1.33.7
third_version=1.33.7
"""

def test_limit_2():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("version.ini", "w", encoding="utf-8") as v:
            v.write("""\
first_version=1.33.7
second_version=1.33.7
third_version=1.33.7
""")
        result = runner.invoke(bamp, ["patch", "-v", "1.33.7", "-f", "version.ini", "-l", "2"])
        assert result.exit_code == 0
        with open("version.ini", "r", encoding="utf-8") as v:
            assert v.read() == """\
first_version=1.33.8
second_version=1.33.8
third_version=1.33.7
"""

def test_limit_0():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("version.ini", "w", encoding="utf-8") as v:
            v.write("""\
first_version=1.33.7
second_version=1.33.7
third_version=1.33.7
""")
        result = runner.invoke(bamp, ["patch", "-v", "1.33.7", "-f", "version.ini", "-l", "0"])
        assert result.exit_code == 0
        with open("version.ini", "r", encoding="utf-8") as v:
            assert v.read() == """\
first_version=1.33.8
second_version=1.33.8
third_version=1.33.8
"""