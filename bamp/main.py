'''
TODO: is newline on windows different for python?
TODO: dry-run? use logging for printing
TODO: treat PART as a custom command
       http://click.pocoo.org/6/commands/#custom-multi-commands ?
'''
import os
import logging
import logging.config

import click

from bamp.engine import bamp_version
from bamp.persistence import bamp_files
from bamp.helpers.callbacks import enable_debug, read_config, required
from bamp.vcs import create_commit, is_tree_clean, make_message
from bamp.helpers.ui import verify_response, ok_exit

logger = logging.getLogger('bamp')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
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
@click.option('vcs', '-V', '--vcs', help='Specify VCS to use.')
@click.option('allow_dirty', '-a', '--allow-dirty', is_flag=True)
@click.option('commit', '-c', '--commit', is_flag=True)
@click.option('message', '-m', '--message')
@click.argument('part', nargs=1,
                type=click.Choice(['patch', 'minor', 'major']))
def bamp(version, part, files, vcs, allow_dirty, commit, message):
    sanity_checks(ROOT_PATH)

    new_version = bamp_version(version, part)
    bamp_files(version, new_version, files)

    if commit:
        commit_message = make_message(message, version, new_version)
        create_commit(vcs, files, commit_message)

    ok_exit('New version: {0}'.format(new_version))


@verify_response
def sanity_checks(root_path):
    """Run environment and configuration sanity checks

    :param root_path: path to the vcs repo dir
    :type root_path: str
    :returns: True, [] if env is sane, False and error message otherwise
    :rtype: tuple(bool, str)

    """
    ctx = click.get_current_context()
    if ctx.params.get('commit'):
        is_tree_clean(ctx.params.get('vcs'), root_path)

    return True, []

if __name__ == '__main__':
    bamp()
