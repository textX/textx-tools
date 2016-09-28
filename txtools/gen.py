import os
import pkg_resources
import click
from collections import namedtuple
from jinja2 import Environment, PackageLoader
from textx.model import all_of_type
from textx.lang import get_language


# An instance of this namedtuple must be registered in textx_gen entry point.
GenDesc = namedtuple('GenDesc', 'name lang callable')


def iter_generators():
    """
    Iterates overs registered generators and returns setuptools EntryPoint
    instances.
    """
    for ep in pkg_resources.iter_entry_points(group='textx_gen'):
        yield ep


def generate(model, lang, package_name, genconf_rules, output_folder):
    """
    Runs generator rules contained in genconf_model using model as the source.

    Args:
        model (input textX model):
        lang (str): The name of the registered language.
        package_name (str): The name of the generator package.
        genconf_rules: A list of genconf rules.
        output_folder (str): The output root path where code should be
            generated.
    """

    meta = get_language(lang)
    env = Environment(loader=PackageLoader(package_name, 'templates'))

    for rule in genconf_rules:

        objs = all_of_type(meta, model, rule.type)
        t = env.get_template(rule.template_path)


        params = {}
        if rule.all:
            # Target file expr must be a single string for "all" rules
            if rule.target_file_expr.__class__.__name__ == 'AttributeReference':
                raise Exception('"all" rules can\'t use Attribute references')
            output_file = os.path.join(output_folder, rule.target_file_expr)
            click.echo("Generating {}".format(output_file))
            os.mkdirs(os.path.dirname(output_file))
            params[rule.var_name] = objs
            with open(output_file, 'w') as f:
                f.write(t.render(**params))
        else:
            for obj in objs:
                output_file = os.path.join(
                    output_folder,
                    evaluate_target(rule.target_file_expr))
                click.echo("Generating {}".format(output_file))
                os.mkdirs(os.path.dirname(output_file))
                params[rule.var_name] = obj
                with open(output_folder, 'w') as f:
                    f.write(t.render(**params))


def merge_genconfs(*models):
    """
    Merges multiple genconf models. Later model's rules will have precedence
    over former ones. Think of it as rule override. This enables user to
    redefine genconf rules defined by the generator component.

    Returns a list of genconf rules.
    """

    rules = {}

    for model in models:
        for rule in model.rules:
            rules[rule.name] = rule

    return rules.values()


def evaluate_target(target_expr, obj):
    """
    Evaluates TargetFilePatheExpression from genconf model.
    """

    retval = []
    for op in target_expr:
        if op.__class__.__name__ == 'AttributeReference':
            retval.append(getattr(obj, op.split('.')[-1]))
        else:
            retval.append(op)

    return "".join(retval)
