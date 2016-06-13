'''
TODO: is newline on windows different for python?

'''
import logging

from bamp.config import find_config, parse_config, make_default_map
from bamp.engine import bamp_version

import click

logger = logging.getLogger(__name__)
logging.basicConfig()


@click.command()
@click.option('version', '--version')
@click.argument('part', type=click.Choice(['patch', 'minor', 'major']))
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def bamp(version, part, files):
    input_args = locals()  # TODO: other way to grab args?
    # TODO: any argument that is required but can be configured
    # can't be marked required. Thus merge function should validate
    # if we have all needed args.
    logger.debug(input_args)
    print(bamp_version(version, part, files))

if __name__ == '__main__':
    # make deault_map out of config
    config = parse_config(find_config())
    print(make_default_map(config))
    bamp(default_map=make_default_map(config))
