'''
TODO: is newline on windows different for python?
TODO: pass config as an option, see aliases.py from click examples

'''
import logging

from bamp.config import find_config, parse_config, make_default_map
from bamp.engine import bamp_version

import click

logger = logging.getLogger(__name__)
logging.basicConfig()


@click.command()
@click.option('version', '--version')
@click.option('files', '-f', type=click.Path(exists=True), multiple=True)
@click.argument('part', nargs=1, type=click.Choice(['patch', 'minor', 'major']))
def bamp(version, part, files):
    # TODO: any argument that is required but can be configured
    # can't be marked required. Thus merge function should validate
    # if we have all needed args.
    print(bamp_version(version, part, files))

if __name__ == '__main__':
    config = parse_config(find_config())
    bamp(default_map=make_default_map(config))
