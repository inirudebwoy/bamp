from click.testing import CliRunner

from bamp.main import main


def test_arg_part_missing():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 2
    assert 'Missing argument "part"' in result.output


def test_arg_part():
    runner = CliRunner()
    result = runner.invoke(main, ['patch'])
    assert result.exit_code == 0


def test_arg_unsupported_part():
    runner = CliRunner()
    result = runner.invoke(main, ['foobar'])
    assert result.exit_code == 1
    assert 'Invalid value for "part"' in result.output


def test_arg_part_with_file():
    runner = CliRunner()
    result = runner.invoke(main, ['major', 'setup.py'])
    assert result.exit_code == 0
    assert 'setup.py' in result.output


def test_arg_part_with_two_files():
    runner = CliRunner()
    result = runner.invoke(main, ['major', 'setup.py', 'tox.ini'])
    assert result.exit_code == 0
    assert 'setup.py' in result.output
    assert 'tox.ini' in result.output
