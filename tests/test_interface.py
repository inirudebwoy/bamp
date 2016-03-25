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
