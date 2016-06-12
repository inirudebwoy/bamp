from StringIO import StringIO
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

from bamp.config.ini import config_dump


def make_config(content):
    config = ConfigParser()
    input_file = StringIO(content)
    config.readfp(input_file)
    return config


def test_empty_config():
    config = make_config('')
    assert {} == config_dump(config)


def test_one_section_no_values():
    config = make_config('[test_section]')
    assert {'test_section': {}} == config_dump(config)


def test_one_section_simple_value():
    config = make_config('[market]\n'
                         'cheese = cheddar')
    assert {'market': {'cheese': 'cheddar'}} == config_dump(config)


def test_one_section_multiline_value():
    config = make_config('[market]\n'
                         'cheeses=\n'
                         '  leicester\n'
                         '  cheddar')
    assert {'market':
            {'cheeses': ['leicester', 'cheddar']}} == config_dump(config)


def test_two_sections_one_empty():
    config = make_config('[empty]\n'
                         '[market]\n'
                         'cheeses=\n'
                         '  leicester\n'
                         '  cheddar')
    assert {'empty': {},
            'market':
            {'cheeses': ['leicester', 'cheddar']}} == config_dump(config)


def test_two_sections_both_multiline_value():
    config = make_config('[market]\n'
                         'cheeses=\n'
                         '  leicester\n'
                         '  cheddar\n'
                         '[fire_department]\n'
                         'shoes=\n'
                         '  brown\n'
                         '  size9')
    assert {'market':
            {'cheeses': ['leicester', 'cheddar']},
            'fire_department':
            {'shoes': ['brown', 'size9']}} == config_dump(config)



