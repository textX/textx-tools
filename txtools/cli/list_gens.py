import click
from txtools.gen import iter_generators


@click.command()
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print description of each generator.')
def list_gens(verbose):
    """
    Lists registered textX code generators.
    """
    for ep in iter_generators():
        gendesc = ep.load()
        desc = ""
        if verbose:
            gen_doc = gendesc.callable.__doc__
            if gen_doc:
                desc = "\n\t{}".format(gen_doc.strip())
        click.echo("%s (%s) - %s (%s)%s" % (gendesc.name, gendesc.lang, ep.dist,
                                            ep.dist.location, desc))
