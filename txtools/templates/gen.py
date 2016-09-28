import os
from txtools.gen import GenDesc, generate
from textx.lang import get_language


def gen(model, output_folder):
    """
    {{package_name}} generator for {{lang_name}} language.
    """
    gc_meta = get_language("genconf")
    curr_dir = os.path.dirname(__file__)
    gc_model = gc_meta.model_from_file(
        os.path.join(curr_dir, '{{package_name}}.genconf'))
    generate(model, "{{lang_name}}", "{{package_name}}", gc_model.rules,
             output_folder)


# This object is registered in setup.py under entry point textx_gen
gendesc = GenDesc(name="{{package_name}}", lang="{{lang_name}}", callable=gen)
