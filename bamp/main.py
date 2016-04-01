import click


@click.command()
@click.option('current_version', '--current_version')
@click.argument('part', type=click.Choice(['patch', 'minor', 'major']))
@click.argument('file_', nargs=-1, type=click.Path(exists=True))
def main(current_version, part, file_):
    pass


if __name__ == '__main__':
    main()
