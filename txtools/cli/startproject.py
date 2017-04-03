import os
import sys
import re
import click
from textx.lang import get_language
from textx.exceptions import TextXError
from txtools import copy_scaffolding, render_scaffolding
from txtools.exceptions import TextXToolsError


@click.command()
@click.option('-t', '--project-type', default='app',
              type=click.Choice(['lang', 'gen', 'app']))
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
                click.echo('There was an error loading language "{}".'
                           .format(language))
                click.echo('Is it installed? Try to install it '
                           'with "pip install textx-lang-{}"'
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
    elif project_type == 'gen':
        package_name = "{}_{}".format(
            language, _project_name_to_package_name(project_name))
        full_project_name = 'textx-{}-{}-{}'.format(project_type,
                                                    language,
                                                    project_name)
    else:
        package_name = _project_name_to_package_name(project_name)
        full_project_name = project_name

    project_type_full = {
        'lang': 'language',
        'gen': 'generator'
    }.get(project_type, project_type)

    click.echo('Generating {} project "{}" in folder "{}".'
               .format(project_type_full, project_name, full_project_name))

    context = {
        'project_name': project_name,
        'full_project_name': full_project_name,
        'package_name': package_name,
        'project_type': project_type,
        'language': language
    }

    try:
        _generate_project(context)
    except TextXToolsError as e:
        click.echo(e)
        sys.exit(1)

    click.echo('Done.')


def _generate_project(context):
    """
    Generates project scaffolding.
    """

    current_dir = os.curdir
    project_folder = os.path.join(current_dir, context['full_project_name'])
    project_type = context['project_type']
    package_name = context['package_name']

    try:
        os.makedirs(project_folder)
    except FileExistsError:
        raise TextXToolsError('Error: Project folder "{}" already exists.'
                                  .format(project_folder))

    # Copy generic part defined in "all" folder
    copy_scaffolding("all", project_folder, package_name)

    # Render generic templates "all" folder
    render_scaffolding("all", project_folder, package_name, context)

    # Copy project type specific
    copy_scaffolding(project_type, project_folder, package_name)

    # Render project type specific
    render_scaffolding(project_type, project_folder, package_name, context)


def _check_project_name(project_name):
    return re.match('^[a-zA-Z][a-zA-Z0-9-]*[a-zA-Z0-9]$', project_name)


def _project_name_to_package_name(project_name):
    """
    Package name contains only lowercase letters and digits.
    """
    return project_name.lower().replace('-', '')
