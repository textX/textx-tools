import pkg_resources
from collections import namedtuple

# An instance of this namedtuple must be registered in textx_gen entry point.
GenDesc = namedtuple('GenDesc', 'name lang callable')


def iter_generators():
    """
    Iterates overs registered generators and returns setuptools EntryPoint
    instances.
    """
    for ep in pkg_resources.iter_entry_points(group='textx_gen'):
        yield ep


