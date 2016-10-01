from __future__ import unicode_literals
import os
import sys
import click
from textx.model import all_of_type
from textx.lang import get_language
from textx.metamodel import metamodel_from_file
from txtools.gen import get_generator_desc
from txtools.exceptions import TextXToolsException

if sys.version < '3':
    text = unicode
else:
    text = str


__all__ = ['load_genconf', 'generate']


genconf_mm = None
PARAMETER_NAMES = ('flask_admin', 'composite_keys')


def meta():
    """
    Language for generators configuration.
    """
    global genconf_mm

    curr_dir = os.path.dirname(__file__)
    if genconf_mm is None:
        genconf_mm = metamodel_from_file(os.path.join(curr_dir, 'genconf.tx'))

    return genconf_mm


def load_genconf(genconf_path):
    """
    Loads genconf model from the given path. Merge with generator genconf.
    Given user genconf rules have precedence over generator provided.

    Returns genconf model.
    """

    mm = meta()
    model = mm.model_from_file(genconf_path)

    # Check params
    for p in model.params:
        if p.name not in PARAMETER_NAMES:
            raise TextXToolsException('Invalid generator parameter "{}".'
                                      .format(p.name))

    # Determine generator name from the file name if not given in the model.
    if not model.gen_name:
        model.gen_name = os.path.splitext(os.path.basename(genconf_path))[0]

    # If output is not given it defaults to 'src'
    if not model.output:
        model.output = 'src'

    gen_desc = get_generator_desc(model.gen_name)

    # Sanity check.
    if gen_desc is None:
        raise TextXToolsException(
            'Generator "{}" for genconf model "{}" is not registered.'.format(
                model.gen_name, genconf_path))

    # Load original genconf from the generator
    orig_genconf_model = gen_desc.genconf()

    # Merge/override by user rules
    merged_rules = _merge_genconfs(orig_genconf_model, model)
    model.rules = merged_rules

    return model


def generate(genconf_model, project_folder):
    """
    Interprets genconf model.

    Args:
        genconf_model (genconf textX model):
        project_folder (str):
    """

    gendesc = get_generator_desc(genconf_model.gen_name)
    meta = get_language(gendesc.lang)

    # Path for templates overrides
    templates_path = os.path.join(project_folder, 'templates',
                                  genconf_model.gen_name)

    output_root = os.path.join(project_folder, genconf_model.output)

    # For each model configured in the current genconf
    for model_path in genconf_model.models:

        click.echo('Processing model "{}"'.format(model_path))
        model = meta.model_from_file(os.path.join(project_folder, 'model',
                                                  model_path))

        for rule in genconf_model.rules:

            # Sanity check
            if len(rule.types) != len(rule.var_names):
                raise TextXToolsException('Number of variables don\'t match'
                                          ' number of types in rule "{}"'
                                          .format(rule.name))

            type_objs = []
            for t in rule.types:
                type_objs.append(all_of_type(meta, model, t))

            params = {}
            if rule.all:
                # Target file expr must be a single string for "all" rules
                if len(rule.target_file_expr.op) > 1 or \
                        type(rule.target_file_expr.op[0]) is not text:
                    raise TextXToolsException(
                        '"all" rules target filename must be string.')
                output_file = os.path.join(output_root, rule.target_file_expr.op[0])
                click.echo("Generating {}".format(output_file))
                try:
                    os.makedirs(os.path.dirname(output_file))
                except FileExistsError:
                    pass

                for ind, obj in enumerate(type_objs):
                    params[rule.var_names[ind]] = obj
                with open(output_file, 'w') as f:
                    f.write(gendesc.render(rule.template_path, params,
                                           templates_path))

            else:
                if len(rule.types) > 1:
                    raise TextXToolsException('Multiple types/variables are not'
                                              ' possible for "non-all" rules.')
                for obj in type_objs[0]:
                    output_file = os.path.join(
                        output_root,
                        evaluate_target(rule.target_file_expr))
                    click.echo("Generating {}".format(output_file))
                    try:
                        os.makedirs(os.path.dirname(output_file))
                    except FileExistsError:
                        pass

                    params[rule.var_names[0]] = obj
                    with open(output_file, 'w') as f:
                        f.write(gendesc.render(rule.template_path, params,
                                               templates_path))


def _merge_genconfs(*models):
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
