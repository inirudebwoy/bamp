'''
TODO: is newline on windows different for python


'''

import logging

from bamp.config import find_config, parse_config
from bamp.engine import bamp_version

import click

logger = logging.getLogger(__name__)
logging.basicConfig()


@click.command()
@click.option('version', '--version')
@click.argument('part', type=click.Choice(['patch', 'minor', 'major']))
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('--debug/--no-debug', default=False)
def main(version, part, files, debug):
    if debug:
        logger.setLevel(logging.DEBUG)

    input_args = locals()  # TODO: other way to grab args?
    logger.debug(input_args)
    params = parse_config(find_config(), input_args)
    logger.debug(params)
    # TODO: this function, or module should handle merge of config and
    # command line arguments
    print(bamp_version(version, part, files))

if __name__ == '__main__':
    main()
