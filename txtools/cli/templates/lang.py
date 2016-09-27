import os
from textx.metamodel import metamodel_from_file


meta = None


def main():
    """
    {{lang_name}} language.
    """
    global meta

    if meta is None:
        curr_dir = os.path.dirname(__file__)
        meta = metamodel_from_file(os.path.join(curr_dir, '{{metamodel_file}}'))

    return meta


