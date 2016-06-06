from bamp.engine import bamp_version, replace
from bamp.config import get_config_path, parse_config

import click


@click.command()
@click.option('current_version', '--current_version')
@click.argument('part', type=click.Choice(['patch', 'minor', 'major']))
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def main(current_version, part, files):
    config_path = get_config_path()
    config = parse_config(config_path)  # TODO: merge with command line?
    bamped = bamp_version(current_version, part, config)
    print(bamped)
    replace(files, current_version, bamped)


if __name__ == '__main__':
    main()
