'''
TODO: is newline on windows different for python?
TODO: dry-run? use logging for printing

'''
import logging
import logging.config

import click

from bamp.engine import bamp_version
from bamp.persistence import bamp_files
from bamp.callbacks import enable_debug, read_config, required

logger = logging.getLogger('bamp')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--debug', help='Enable debug flag.', is_flag=True,
              expose_value=False, callback=enable_debug, is_eager=True)
@click.option('--config', type=click.Path(exists=True, dir_okay=False),
              help='Path to a config file.',
              callback=read_config, expose_value=False)
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
    new_version = bamp_version(version, part)
    bamp_files(version, new_version, files)
    # TODO: VC goes here, if config is set
    click.echo(new_version)

if __name__ == '__main__':
    bamp()
