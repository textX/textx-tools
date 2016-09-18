import click
from textx.lang import iter_languages


@click.command()
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print description of each language.')
def list_langs(verbose):
    """
    Lists registered textX languages.
    """
    for ep in iter_languages():
        desc = ""
        if verbose:
            lang_doc = ep.load().__doc__
            if lang_doc:
                desc = "\n\t{}".format(lang_doc.strip())

        click.echo("%s - %s (%s)%s" % (ep.name, ep.dist, ep.dist.location,
                                       desc))
