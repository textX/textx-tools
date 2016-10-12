
import click
from textx.metamodel import metamodel_from_file
from textx.lang import get_language
from textx.exceptions import TextXError
from txtools.vis import metamodel_export, model_export


@click.command()
@click.argument('model_file')
@click.option('-l', '--language', default='textx',
              help='Registered language name. '
              'Default is "textx" - for textX grammars.')
@click.option('-d', '--debug', default=False, is_flag=True,
              help='run in debug mode')
def vis(model_file, language, debug):
    """
    Visualize (meta)model using dot.
    """
    try:
        if language == 'textx':
            mm = metamodel_from_file(model_file, debug=debug)
            click.echo("Generating '%s.dot' file for meta-model." % model_file)
            click.echo("To convert to PDF run 'dot -Tpdf -O %s.dot'"
                       % model_file)
            metamodel_export(mm, "%s.dot" % model_file)
        else:
            mm = get_language(language)
            model = mm.model_from_file(model_file, debug=debug)
            click.echo("Generating '%s.dot' file for model." % model_file)
            click.echo("To convert to PDF run 'dot -Tpdf -O %s.dot'"
                       % model_file)
            model_export(model, "%s.dot" % model_file)
    except TextXError as e:
        click.echo(e)
