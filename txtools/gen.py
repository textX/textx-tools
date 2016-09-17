import pkg_resources


def iter_generators():
    """
    Iterates overs registered generators and returns setuptools EntryPoint
    instances.
    """
    for ep in pkg_resources.iter_entry_points(group='textx_generators'):
        yield ep
