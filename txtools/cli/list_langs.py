import click
from textx.lang import iter_languages


@click.command()
def list_langs():
    """
    Lists registered textX languages.
    """
    for ep in iter_languages():
        click.echo("%s - %s (%s)" % (ep.name, ep.dist, ep.dist.location))
