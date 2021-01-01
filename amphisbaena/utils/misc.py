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
    module, name = path.rsplit(".", 1)
    module_ = import_module(module)
    return getattr(module_, name)
