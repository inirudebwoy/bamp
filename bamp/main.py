from bamp.config import find_config, parse_config
from bamp.engine import bamp_version

import click


@click.command()
@click.option('version', '--version')
@click.argument('part', type=click.Choice(['patch', 'minor', 'major']))
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def main(version, part, files):
    input_args = locals()  # TODO: other way to grab args?
    params = parse_config(find_config(), input_args)
    # TODO: config will include multiline values as file input lists, split('\n')
    # TODO: is newline on windows different for python?
    # TODO: this function, or module should handle merge of config and command line arguments
    print(bamp_version(version, part, params))

if __name__ == '__main__':
    main()
