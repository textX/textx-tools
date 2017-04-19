import os
import shutil
import click
from jinja2 import Environment, FileSystemLoader

__version__ = "0.1.dev0"


def copy_scaffolding(project_type, project_folder, package_name):
    """
    Copies all files from the copy folder of scaffolding templates.
    """
    import txtools
    root_folder = os.path.join(os.path.dirname(txtools.__file__), 'templates',
                               project_type, 'copy')
    for root, dirs, files in os.walk(root_folder, topdown=True):
        [dirs.remove(d) for d in list(dirs) if d in ['__pycache__']]
        for f in files:
            src_file = os.path.join(root, f)
            rel_path = os.path.relpath(src_file, root_folder)
            target_file = os.path.join(project_folder, rel_path)\
                .replace('pack_name', package_name)
            try:
                os.makedirs(os.path.dirname(target_file))
            except FileExistsError:
                pass
            click.echo('Creating {}'
                       .format(rel_path.replace('pack_name', package_name)))
            shutil.copy(src_file, target_file)


def render_scaffolding(project_type, project_folder, package_name, context):
    """
    Renders all jinja templates from the jinja folder of scaffolding templates.
    """
    import txtools
    root_folder = os.path.join(os.path.dirname(txtools.__file__), 'templates',
                               project_type, 'jinja')
    env = Environment(loader=FileSystemLoader(root_folder))
    for root, dirs, files in os.walk(root_folder, topdown=True):
        [dirs.remove(d) for d in list(dirs) if d in ['__pycache__']]
        for f in files:
            src_file = os.path.join(root, f)
            rel_path = os.path.relpath(src_file, root_folder)
            target_file = os.path.join(project_folder, rel_path)\
                .replace('pack_name', package_name)
            try:
                os.makedirs(os.path.dirname(target_file))
            except FileExistsError:
                pass
            click.echo('Creating {}'
                       .format(rel_path.replace('pack_name', package_name)))
            with open(target_file, 'w') as f:
                f.write(env.get_template(rel_path).render(**context))
