import click
from textx.metamodel import metamodel_from_file
from textx.lang import get_language
from textx.exceptions import TextXError


@click.command()
@click.argument('model_file')
@click.option('-l', '--language', default='textx',
              help='Registered language name. '
              'Default is "textx" - for textX grammars.')
@click.option('-d', '--debug', default=False, is_flag=True,
              help='run in debug mode')
def check(language, model_file, debug):
    """
    Checks (meta)model syntax validity.
    """
    try:
        if language == 'textx':
            click.echo('Checking model using language "textx".')
            metamodel_from_file(model_file, debug=debug)
            click.echo('Meta-model OK.')
        else:
            mm = get_language(language)
            click.echo('Checking model using language "{}".'.format(language))
            mm.model_from_file(model_file, debug=debug)
            click.echo('Model OK.')
    except TextXError as e:
        click.echo(e)
