import os
from textx.metamodel import metamodel_from_file
from txtools.gen import get_generator_desc
from txtools.exceptions import TextXToolsException


genconf_mm = None


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

    # Determine generator name from the file name if not given in the model.
    if not model.gen_name:
        model.gen_name = os.path.splitext(os.path.basename(genconf_path))[0]

    gen_desc = get_generator_desc(model.gen_name)

    # Sanity check.
    if gen_desc is None:
        raise TextXToolsException(
            'Generator "{}" for genconf model "{}" is not valid.'.format(
                model.gen_name, genconf_path))

    # Load original genconf from the generator
    orig_genconf_model = gen_desc.genconf()

    # Merge/override by user rules
    merged_rules = _merge_genconfs(orig_genconf_model, model)
    model.rules = merged_rules

    return model


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


