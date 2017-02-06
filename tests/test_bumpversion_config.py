from six import StringIO
from six.moves import configparser

from bamp.config.bumpversion import config_dump


def make_config(content):
    config = configparser.ConfigParser()
    input_file = StringIO(content)
    config.readfp(input_file)
    return config


def test_empty_config():
    config = make_config('')
    assert {} == config_dump(config)


def test_one_section_no_values():
    config = make_config('[bumpversion]')
    assert {} == config_dump(config)


def test_one_section_simple_value():
    config = make_config('[bumpversion]\n' 'cheese = cheddar')
    assert {'cheese': 'cheddar'} == config_dump(config)


def test_one_file_section():
    config = make_config('[bumpversion:files:./file_one.php]')
    assert {'files': ('./file_one.php', )} == config_dump(config)


def test_two_file_sections():
    config = make_config('[bumpversion:files:./file_one.php]\n'
                         '[bumpversion:files:./file_two.php]')
    assert {
        'files': ('./file_one.php', './file_two.php')
    } == config_dump(config)


def test_current_version_renamed():
    config = make_config('[bumpversion]\n' 'current_version = 1.0.42')
    assert {'version': '1.0.42'} == config_dump(config)
