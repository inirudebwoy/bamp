'''
TODO: is newline on windows different for python?
TODO: pass config as an option, see aliases.py from click examples
TODO: dry-run? use logging for printing

'''
import logging

import click

from bamp.config import find_config, parse_config, make_default_map
from bamp.engine import bamp_version, bamp_files

logger = logging.getLogger(__name__)
logging.basicConfig()


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
@click.option('-v', '--version', help='Current version of the program.',
              callback=required)
@click.option('files', '-f', '--file',
              help=('File where version can be found. '
                    'Can be used multiple times.'),
              type=click.Path(exists=True), multiple=True,
              callback=required)
@click.argument('part', nargs=1,
                type=click.Choice(['patch', 'minor', 'major']))
def bamp(version, part, files):
    new_version = bamp_version(version, part, files)
    bamp_files(version, new_version, files)
    # TODO: VC goes here, if config is set
    click.echo(new_version)

if __name__ == '__main__':
    config = parse_config(find_config())
    bamp(default_map=make_default_map(config))
