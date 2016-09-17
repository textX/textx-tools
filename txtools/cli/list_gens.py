import click
from txtools.gen import iter_generators


@click.command()
def list_gens():
    """
    Lists registered textX code generators.
    """
    for ep in iter_generators():
        click.echo("%s - %s (%s)" % (ep.name, ep.dist, ep.dist.location))
