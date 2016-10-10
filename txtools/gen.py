"""
Generator registration and query support.
"""
import pkg_resources
from collections import namedtuple


# An instance of this namedtuple must be registered in textx_gen entry point.
GenDesc = namedtuple('GenDesc', 'name lang desc genconf render validate')


def iter_generators():
    """
    Iterates over registered generators and returns setuptools EntryPoint
    instances.
    """
    for ep in pkg_resources.iter_entry_points(group='textx_gen'):
        yield ep


def get_generator_desc(generator_name):

    for ep in iter_generators():
        gen_desc = ep.load()
        if gen_desc.name == generator_name:
            return gen_desc
