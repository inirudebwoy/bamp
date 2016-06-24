'''
TODO: is newline on windows different for python?
TODO: pass config as an option, see aliases.py from click examples
TODO: dry-run? use logging for printing

'''
import logging
import logging.config
import sys

import click

from bamp.config import find_config, prepare_config, make_default_map
from bamp.engine import bamp_version
from bamp.persistence import bamp_files
from bamp.exc import ErrorConfigParsing


DEBUG = False


class MyFilter(logging.Filter):
    def __init__(self, debug=None):
        self.debug = debug

    def filter(self, record):
        # TODO: Debug mode here should print everything
        # I want to display exception messages to a user but with no traceback
        # with filter on a handler I should be able to do it.
        # pass errors and info(?) to StreamHandler, rest to null unless in Debug mode.
        # than everything is getting printed out.
        if self.debug:
            return True

        if record.levelname == 'ERROR' and record.exc_info:
            record.exc_info = None
        return True

LOGGING = {
    'version': 1,
    'filters': {
        'myfilter': {
            '()': MyFilter,
            'debug': DEBUG
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['myfilter']
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    },
}


def required(ctx, param, value):
    """Make sure that option passed in has value

    Some options can be passed from the command line, using flags, like
    --version or be retrieved from config file. Function makes sure
    that passed option has a value.

    """
    if not value:
        raise click.UsageError(
            '"%(name)s" is required. Add to config or pass with %(flag)s '
            'option.' % {'name': param.name,
                         'flag': param.opts})
    return value

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--debug', is_flag=True)
@click.option('-v', '--version', help='Current version of the program.',
              callback=required)
@click.option('files', '-f', '--file',
              help=('File where version can be found. '
                    'Can be used multiple times.'),
              type=click.Path(exists=True), multiple=True,
              callback=required)
@click.argument('part', nargs=1,
                type=click.Choice(['patch', 'minor', 'major']))
def bamp(version, part, files, debug):
    new_version = bamp_version(version, part)
    bamp_files(version, new_version, files)
    # TODO: VC goes here, if config is set
    click.echo(new_version)

if __name__ == '__main__':
    if '--debug' in sys.argv:
        DEBUG = True
        LOGGING['filters']['myfilter']['debug'] = DEBUG

    logging.config.dictConfig(LOGGING)

    try:
        config = prepare_config(find_config())
    except KeyboardInterrupt:
        click.echo('User cancelled.')
    except ErrorConfigParsing:
        sys.exit(1)
    bamp(default_map=make_default_map(config))
