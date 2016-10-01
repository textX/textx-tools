import os
from jinja2 import Environment, PackageLoader, FileSystemLoader, ChoiceLoader
from txtools.gen import GenDesc
from textx.lang import get_language
from txtools.exceptions import TextXToolsException


PARAM_NAMES = ()


def genconf_model():
    """
    Returns genconf model for '{{package_name}}' generator and '{{language}}'
    language.
    """
    gc_meta = get_language("genconf")
    curr_dir = os.path.dirname(__file__)
    gc_model = gc_meta.model_from_file(
        os.path.join(curr_dir, '{{package_name}}.genconf'))

    # Check parameters
    for p in gc_model.params:
        if p.name not in PARAM_NAMES:
            raise TextXToolsException('Undefined generator parameter "{}".'
                                      .format(p.name))


def render(template_path, context, root_path=None):
    """
    Returns rendered template. By default search for template at the given
    root path. If not found search is continued in the generator templates
    folder.

    Args:
        template_path (str): Relative path to the template inside the root_path.
        context (dict)
        root_path (str): The root where templates should be searched first.
            If None no override is performed.
    """

    # By default jinja2 is used but this can be changed by the user.
    env = Environment(loader=ChoiceLoader([
        FileSystemLoader(root_path),
        PackageLoader('{{package_name}}', 'templates')
    ]))

    return env.get_template(template_path).render(**context)


# This object is registered in setup.py under entry point textx_gen
gendesc = GenDesc(name="{{package_name}}", lang="{{language}}",
                  desc="{{package_name}} generator for {{language}} language",
                  genconf=genconf_model, render=render,
                  param_names=PARAM_NAMES)
