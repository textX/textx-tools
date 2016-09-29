import os
from jinja2 import Environment, PackageLoader, FileSystemLoader, ChoiceLoader
from txtools.gen import GenDesc
from textx.lang import get_language


def genconf_model():
    """
    Returns genconf model for {{package_name}} generator and {{lang_name}}
    language.
    """
    gc_meta = get_language("genconf")
    curr_dir = os.path.dirname(__file__)
    return gc_meta.model_from_file(
        os.path.join(curr_dir, '{{package_name}}.genconf'))


def render(root_path, template_path, context):
    """
    Returns rendered template. By default search for template at the given
    root path. If not found search is continued in the generator templates
    folder.

    Args:
        root_path (str): The root where templates should be searched first.
        template_path (str): Relative path to the template inside the root_path.
        context (dict)
    """

    # By default jinja2 is used but this can be changed by the user.
    env = Environment(loader=ChoiceLoader([
        FileSystemLoader(root_path),
        PackageLoader('{{package_name}}', 'templates')
    ]))

    return env.get_template(template_path).render(**context)


# This object is registered in setup.py under entry point textx_gen
gendesc = GenDesc(name="{{package_name}}", lang="{{language}}",
                  genconf=genconf_model, render=render)
