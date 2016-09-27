import os
import sys
import re
import click
from jinja2 import Environment, PackageLoader
from textx.lang import get_language
from textx.exceptions import TextXError


@click.command()
@click.option('-t', '--project-type', default='lang',
              type=click.Choice(['lang', 'gen']))
@click.option('-l', '--language',
              help='Language for generator projects.')
@click.argument('project_name')
def startproject(project_type, language, project_name):
    """
    Generates scaffolding for textX projects.
    """
    if project_type == 'gen':
        if not language:
            click.echo('Language must be specified for generator'
                       ' projects. See -l switch.')
            sys.exit(1)
        else:
            try:
                get_language(language)
            except TextXError as e:
                click.echo(e)
                click.echo('Try to install it with "pip install textx-lang-{}"'
                           .format(language))
                click.echo('Use "textx list-langs" to see all registered '
                           'languages.')
                sys.exit(1)

    if not _check_project_name(project_name):
        click.echo('Project name may contain letters, digits and dashes.')
        sys.exit(1)

    if project_type == 'lang':
        package_name = _project_name_to_package_name(project_name)
        full_project_name = 'textx-{}-{}'.format(project_type, project_name)
    else:
        package_name = "{}_{}".format(
            language, _project_name_to_package_name(project_name))
        full_project_name = 'textx-{}-{}-{}'.format(project_type,
                                                    language,
                                                    project_name)

    project_type_full = 'language' if project_type == 'lang' else 'generator'

    click.echo('Generating project for {} {} in folder {}.'
               .format(project_type_full, project_name, full_project_name))

    _generate_base(project_name, full_project_name, package_name)

    if project_type == 'lang':
        _start_lang(project_name, full_project_name, package_name)
    else:
        _start_gen(project_name, full_project_name, package_name, language)

    click.echo('Done.')


def _start_lang(project_name, full_project_name, package_name):
    """
    Generates scaffolding for 'language' textX project.
    """
    current_dir = os.curdir
    project_folder = os.path.join(current_dir, full_project_name)

    env = Environment(loader=PackageLoader('txtools.cli', 'templates'))

    t = env.get_template('setup-lang.py')
    with open(os.path.join(project_folder, 'setup.py'), 'w') as f:
        f.write(t.render(full_project_name=full_project_name,
                         package_name=package_name))

    t = env.get_template('lang.py')
    with open(os.path.join(project_folder, package_name, 'lang.py'), 'w') as f:
        f.write(t.render(metamodel_file='{}.tx'.format(package_name),
                         lang_name=package_name))

    t = env.get_template('lang.tx')
    with open(os.path.join(project_folder, package_name,
                           '{}.tx'.format(package_name)), 'w') as f:
        f.write(t.render())


def _start_gen(project_name, full_project_name, package_name, language):
    """
    Generates scaffolding for 'generator' textX project.
    """
    current_dir = os.curdir
    project_folder = os.path.join(current_dir, full_project_name)

    env = Environment(loader=PackageLoader('txtools.cli', 'templates'))

    t = env.get_template('setup-gen.py')
    with open(os.path.join(project_folder, 'setup.py'), 'w') as f:
        f.write(t.render(full_project_name=full_project_name,
                         package_name=package_name))

    t = env.get_template('gen.py')
    with open(os.path.join(project_folder, package_name, 'gen.py'), 'w') as f:
        f.write(t.render(package_name=package_name, lang_name=language))


def _generate_base(project_name, project_name_full, package_name):
    """
    Generates base scaffolding.
    """
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


