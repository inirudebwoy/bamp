'''
TODO: is newline on windows different for python?
TODO: dry-run? use logging for printing
TODO: treat PART as a custom command
       http://click.pocoo.org/6/commands/#custom-multi-commands ?
TODO: six module?
'''
import sys
import logging
import logging.config

import click

from bamp.engine import bamp_version
from bamp.persistence import bamp_files
from bamp.callbacks import enable_debug, read_config, required
from bamp.vcs import create_commit, is_tree_clean, get_repo, make_commit_message

logger = logging.getLogger('bamp')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


import os


ROOT_PATH = os.path.abspath(os.path.curdir)


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
@click.option('vcs', '-V', '--vcs', help='Specify VCS to use.', default='git')
@click.argument('part', nargs=1,
                type=click.Choice(['patch', 'minor', 'major']))
def bamp(version, part, files, vcs):
    ctx = click.get_current_context()
    result, errors = sanity_checks(ROOT_PATH)
    if not result and errors:
        click.secho(errors, fg='red')
        sys.exit(1)

    new_version = bamp_version(version, part)
    # success = bamp_files(version, new_version, files)
    success, errors = bamp_files(version, new_version, files)
    if not success and errors:
        click.secho(errors)
        sys.exit(1)

    if success and ctx.default_map.get('commit'):
        repo = get_repo(ROOT_PATH)
        message = make_commit_message()
        create_commit(vcs, message, files)
    click.secho('New version: {0}'.format(new_version),
                fg='green')


def sanity_checks(root_path):
    ctx = click.get_current_context()
    clean, error = is_tree_clean(ctx.default_map.get('vcs'), root_path)
    if not clean:
        return clean, error

if __name__ == '__main__':
    bamp()
