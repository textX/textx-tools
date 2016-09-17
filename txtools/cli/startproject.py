import click


@click.command()
@click.argument('project_type')
def startproject(project_type):
    """
    Generates scafolding for textX project
    """
    click.echo('TODO')
