import os
import sys
import click
from txtools.lang.genconf import load_genconf
from txtools.gen import generate
from txtools.exceptions import TextXToolsException


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
            raise TextXToolsException('There is no "genconf" folder here. '
                                      'Is this a textX project?')

        click.echo("Generating application code.")

        # Load each genconf file. Merge with base genconf for the generator.
        for root, dirs, files in \
                os.walk(os.path.join(project_folder, 'genconf')):
            for f in files:
                _, ext = os.path.splitext(f)
                if not ext == '.genconf':
                    continue
                gc_model = load_genconf(os.path.join(root, f))

                # For each model configured in current genconf
                for model in gc_model.models:
                    generate(model, )

    except TextXToolsException as e:
        click.echo(e)
        sys.exit(1)

    # For each referenced model, load model using appropriate language.
    # Calls generate for the given model and given genconf.
    click.echo("Done.")
