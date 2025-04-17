from fnmatch import fnmatch


def should_ignore(name, patterns):
    """

    :param name:
    :param patterns:
    :return:
    """
    return any(fnmatch(name, p) for p in patterns)