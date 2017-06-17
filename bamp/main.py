'''
TODO: is newline on windows different for python?
TODO: dry-run? use logging for printing
TODO: treat PART as a custom command
       http://click.pocoo.org/6/commands/#custom-multi-commands ?
'''
import logging
import logging.config

import click

from bamp.config import add_config, get_root_path
from bamp.engine import bamp_version
from bamp.helpers import docs
from bamp.helpers.callbacks import enable_debug, read_config, required
from bamp.helpers.ui import ok_exit, verify_response
from bamp.persistence import bamp_files
from bamp.vcs import (create_commit, create_tag, is_tree_clean, make_message,
                      make_tag_name)

logger = logging.getLogger('bamp')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--debug',
    help=docs.DEBUG_OPTION_HELP,
    is_flag=True,
    expose_value=False,
    callback=enable_debug,
    is_eager=True)
@click.option(
    '--config',
    type=click.Path(
        exists=True, dir_okay=False),
    help=docs.CONFIG_OPTION_HELP,
    callback=read_config)
@click.option(
    '-v', '--version', help=docs.VERSION_OPTION_HELP, callback=required)
@click.option(
    'files',
    '-f',
    '--file',
    help=docs.FILES_OPTION_HELP,
    type=click.Path(exists=True),
    multiple=True)
@click.option('vcs', '-V', '--vcs', help=docs.VCS_OPTION_HELP)
@click.option('allow_dirty', '-a', '--allow-dirty', is_flag=True)
@click.option(
    'commit',
    '-c',
    '--commit',
    is_flag=True,
    help=docs.COMMIT_FLAG_OPTION_HELP)
@click.option('message', '-m', '--message', help=docs.MESSAGE_OPTION_HELP)
@click.option(
    'tag', '-t', '--tag', is_flag=True, help=docs.TAG_FLAG_OPTION_HELP)
@click.option(
    'tag_name',
    '-T',
    '--tag-name',
    help=docs.TAG_NAME_OPTION_HELP,
    metavar=docs.TAG_NAME_OPTION_METAVAR)
@click.argument(
    'part', nargs=1, type=click.Choice(['patch', 'minor', 'major']))
@add_config
def bamp(version, part, files, vcs, allow_dirty, commit, message, config, tag,
         tag_name):
    root_path = get_root_path()
    sanity_checks(root_path)

    new_version = bamp_version(version, part)
    bamp_files(version, new_version, files)

    if commit:
        commit_message = make_message(message, version, new_version)
        commit_sha1 = create_commit(vcs, files, commit_message)
    if tag and commit_sha1:
        tag_message = make_tag_name(tag_name, new_version)
        create_tag(vcs, commit_sha1, tag_message)

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
