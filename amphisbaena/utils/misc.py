"""
Miscellaneous functions
"""
from functools import lru_cache
from importlib import import_module
from typing import Any


@lru_cache
def load_object(path: str) -> Any:
    """

    :param path:
    :type path: str
    :return:
    :rtype: Any
    """
    parts = path.rsplit(".", 1)

    module = import_module(parts[0])

    try:
        name = parts[1]
    except IndexError:
        return module
    else:
        return getattr(module, name)
