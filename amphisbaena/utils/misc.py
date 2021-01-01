"""
Miscellaneous functions
"""
from functools import lru_cache
from importlib import import_module
from typing import Any


@lru_cache
def load_object(path: str, *, type_: str = "class") -> Any:
    """

    :param path:
    :type path: str
    :param type_:
    :type type_: str
    :return:
    :rtype: Any
    """
    if type_ in ("class", "function", "variable"):  # class or function
        module, name = path.rsplit(".", 1)
        module_ = import_module(module)
        return getattr(module_, name)

    if type_ == "module":
        return import_module(path)
