from bamp.engine import bamp_version
from bamp.config import get_config_path, parse_config

import click


@click.command()
@click.option('current_version', '--current_version')
@click.argument('part', type=click.Choice(['patch', 'minor', 'major']))
@click.argument('file_', nargs=-1, type=click.Path(exists=True))
def main(current_version, part, file_):
    config_path = get_config_path()
    config = parse_config(config_path)  # TODO: merge with command line?
    print(bamp_version(current_version, part, config))


if __name__ == '__main__':
    main()
