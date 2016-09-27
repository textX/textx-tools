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

    if project_type == 'lang':
        project_type_full = 'language'
        additional_deps = ''
    else:
        project_type_full = 'generator'
        additional_deps = ', "jinja2"'

    click.echo('Generating project for {} {} in folder {}.'
               .format(project_type_full, project_name, full_project_name))

    _generate_base(project_name, full_project_name, project_type,
                   additional_deps)

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


def _generate_base(project_name, project_name_full, project_type,
                   additional_deps):
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

    # generate setup.py
    with open(os.path.join(project_folder, 'setup.py'), 'w') as f:
        f.write(setup_string.format(
            project_name=project_name,
            project_name_full=project_name_full,
            package_name=package_name,
            project_type=project_type,
            additional_deps=additional_deps
        ))

    # generate README.md
    with open(os.path.join(project_folder, 'README.md'), 'w') as f:
        f.write("""#{}

TODO: Write project description.
                """
        )


def _check_project_name(project_name):
    return re.match('^[a-zA-Z][a-zA-Z0-9-]*[a-zA-Z0-9]$', project_name)


def _project_name_to_package_name(project_name):
    """
    Package name contains only lowercase letters and digits.
    """
    return project_name.lower().replace('-', '')


setup_string = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup

__author__ = "TODO <TODO AT somedomain DOT com>"
__version__ = "0.1"

NAME = '{project_name_full}'
DESC = 'TODO'
VERSION = __version__
AUTHOR = 'TODO'
AUTHOR_EMAIL = __author__
LICENSE = 'MIT'
URL = 'https://github.com/TODO/%s' % NAME
DOWNLOAD_URL = 'https://github.com/TODO/%s/archive/v%s.tar.gz' % \
    (NAME, VERSION)
README = codecs.open(os.path.join(os.path.dirname(__file__), 'README.md'),
                     'r', encoding='utf-8').read()

setup(
    name = NAME,
    version = VERSION,
    description = DESC,
    long_description = README,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    maintainer = AUTHOR,
    maintainer_email = AUTHOR_EMAIL,
    license = LICENSE,
    url = URL,
    download_url = DOWNLOAD_URL,
    packages = ["{package_name}"{additional_deps}],
    install_requires = ["textx-tools"],
    keywords = "tools generator language DSL",
    entry_points={{
        'textx_{project_type}': [
            '{package_name} = {package_name}.{project_type}:main',
        ]
    }},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ]

)
"""






