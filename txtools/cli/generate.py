import os
import sys
import click
from txtools.lang.genconf import load_genconf
from txtools.lang import genconf
from txtools.exceptions import TextXToolsError
from textx.exceptions import TextXError


@click.command()
@click.option('-p', '--project_folder', default=None,
              help='Path to project folder. Default is the current folder.')
def generate(project_folder):
    """
    Runs source code generator.
    """
    try:

        project_folder = project_folder if project_folder else os.curdir

        # Check if genconf folder exists
        if not os.path.exists(os.path.join(project_folder, 'genconf')):
            raise TextXToolsError('There is no "genconf" folder here. '
                                      'Is this a textX project?')

        click.echo("Generating application code.")

        for root, dirs, files in \
                os.walk(os.path.join(project_folder, 'genconf')):
            for f in files:
                _, ext = os.path.splitext(f)
                if not ext == '.genconf':
                    continue

                # Load each genconf file. Merge with base genconf for the
                # generator.
                gc_model = load_genconf(os.path.join(root, f))

                # Interpret/generate genconf model
                genconf.generate(gc_model, project_folder)

    except (TextXToolsError, TextXError) as e:
        click.echo("Error: {}".format(e))
        sys.exit(1)

    # For each referenced model, load model using appropriate language.
    # Calls generate for the given model and given genconf.
    click.echo("Done.")
