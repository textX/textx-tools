import os
import click
from txtools.exception import TextXToolsException
from txtools.lang.genconf import load_genconf
from txtools.gen import generate


@click.command()
@click.argument('project_folder', default=None)
def generate(project_folder):
    """
    Runs source code generator.
    """
    project_folder = project_folder \
        if project_folder else os.path.dirname(__file__)

    # Check if genconf folder exists
    if not os.path.exists(os.path.join(project_folder, 'genconf')):
        raise TextXToolsException('There is no "genconf" folder here. '
                                  'Is this a textX project?')

    click.echo("Generating code for the application.")

    # Load each genconf file. Merge with base genconf for the generator.
    for root, dirs, files in os.walk(project_folder):
        for f in files:
            _, ext = os.path.splitext(f)
            if not ext == 'genconf':
                continue
            gc_model = load_genconf(f)

            # For each model configured in current genconf
            for model in gc_model.models:
                generate(model, )


    # For each referenced model, load model using appropriate language.
    # Calls generate for the given model and given genconf.
    click.echo("Done.")
