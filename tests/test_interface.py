from click.testing import CliRunner
from dulwich import porcelain

from bamp.main import bamp


def test_arg_part_missing():
    """bamp"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(bamp)
        assert result.exit_code == 2
        assert 'Missing argument "part"' in result.output


def test_arg_part_no_version():
    """bamp patch"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(bamp, ['patch'])
        assert result.exit_code == 2
        assert '"version" is required.' in result.output


def test_arg_part_with_version():
    """bamp patch -v 0.0.1"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(bamp, ['patch', '-v', '0.0.1'])
        assert result.exit_code == 2
        assert '"files" is required.' in result.output


def test_arg_part_with_version_with_nonexisting_file():
    """bamp patch -v 0.0.1 -f version.ini"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            bamp, ['patch', '-v', '0.0.1', '-f', 'version.ini']
        )
        assert result.exit_code == 2
        assert '"version.ini" does not exist' in result.output


def test_arg_part_with_version_with_existing_file():
    """bamp patch -v 0.0.1 -f version.ini"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('version.ini', 'w') as v:
            v.write('0.0.1')
        result = runner.invoke(
            bamp, ['patch', '-v', '0.0.1', '-f', 'version.ini']
        )
        assert result.exit_code == 0


def test_arg_unsupported_part():
    """bamp foobar"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(bamp, ['foobar'])
        assert result.exit_code == 2
        assert 'Invalid value for "part"' in result.output


def test_with_default_commit_no_vcs():
    """bamp patch -v 0.0.1 -f version.ini -c"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('version.ini', 'w') as v:
            v.write('0.0.1')
        result = runner.invoke(
            bamp, ['patch', '-v', '0.0.1', '-f', 'version.ini', '-c']
        )
        assert result.exit_code == 1


def test_default_tag_default_commit_with_vcs():
    """bamp patch -v 0.0.1 -f version.ini -ct"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        porcelain.init('.')  # create git repo
        with open('version.ini', 'w') as v:
            v.write('0.0.1')
        result = runner.invoke(
            bamp, ['patch', '-v', '0.0.1', '-f', 'version.ini', '-c', '-t']
        )
        assert result.output == 1
        assert result.exit_code == 0
