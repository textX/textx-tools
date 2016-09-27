import os
import re
import click
from jinja2 import Environment, PackageLoader


@click.command()
@click.option('-t', '--project-type', default='lang',
              type=click.Choice(['lang', 'gen']))
@click.argument('project_name')
def startproject(project_type, project_name):
    """
    Generates scaffolding for textX projects.
    """
    if not _check_project_name(project_name):
        raise Exception('Project name may contain letters, digits and dashes.')

    full_project_name = 'textx-{}-{}'.format(project_type, project_name)
    project_type_full = 'language' if project_type == 'lang' else 'generator'

    click.echo('Generating project for {} {} in folder {}.'
               .format(project_type_full, project_name, full_project_name))

    _generate_base(project_name, full_project_name)

    if project_type == 'lang':
        _start_lang(project_name, full_project_name)
    else:
        _start_gen(project_name)

    click.echo('Done.')


def _start_lang(project_name, full_project_name):
    """
    Generates scaffolding for 'language' textX project.
    """
    package_name = _project_name_to_package_name(project_name)

    current_dir = os.curdir
    project_folder = os.path.join(current_dir, full_project_name)

    env = Environment(loader=PackageLoader('txtools.cli', 'templates'))

    t = env.get_template('setup-lang.py')
    with open(os.path.join(project_folder, 'setup.py'), 'w') as f:
        f.write(t.render(full_project_name=full_project_name,
                         package_name=package_name))

    t = env.get_template('lang.py')
    with open(os.path.join(project_folder, package_name, 'lang.py'), 'w') as f:
        f.write(t.render(metamodel_file='{}.tx'.format(package_name)))

    t = env.get_template('lang.tx')
    with open(os.path.join(project_folder, package_name,
                           '{}.tx'.format(package_name)), 'w') as f:
        f.write(t.render())


def _start_gen(project_name):
    """
    Generates scaffolding for 'generator' textX project.
    """


def _generate_base(project_name, project_name_full):
    """
    Generates base scaffolding.
    """

    package_name = _project_name_to_package_name(project_name)

    current_dir = os.curdir
    project_folder = os.path.join(current_dir, project_name_full)

    os.makedirs(project_folder)
    os.makedirs(os.path.join(project_folder, package_name))

    # Generate base package __init__.py file
    open(os.path.join(project_folder, package_name, '__init__.py'), 'w').close()

    # generate README.md
    with open(os.path.join(project_folder, 'README.md'), 'w') as f:
        f.write("""# {}

TODO: Write project description.
                """.format(project_name))


def _check_project_name(project_name):
    return re.match('^[a-zA-Z][a-zA-Z0-9-]*[a-zA-Z0-9]$', project_name)


def _project_name_to_package_name(project_name):
    """
    Package name contains only lowercase letters and digits.
    """
    return project_name.lower().replace('-', '')


