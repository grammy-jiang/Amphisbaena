"""
Miscellaneous functions
"""
import asyncio
import functools
from functools import lru_cache
from importlib import import_module
from typing import Any, Callable


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


@lru_cache
def to_sync(func: Callable) -> Callable:
    """
    A decorator to convert function to sync
    :param func:
    :type func: Callable
    :return:
    :rtype: Callable
    """
    loop = asyncio.get_event_loop()

    def convert_to_sync(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            return loop.run_until_complete(func(*args, **kwargs))
        else:
            return func(*args, **kwargs)

    return convert_to_sync


@lru_cache
def to_async(func: Callable, executor=None) -> Callable:
    """

    :param func:
    :type func: Callable
    :param executor:
    :type executor:
    :return:
    :rtype: Callable
    """
    loop = asyncio.get_event_loop()
    if asyncio.iscoroutinefunction(func):

        async def convert_to_async(*args, **kwargs):
            return await func(*args, **kwargs)

    else:

        async def convert_to_async(*args, **kwargs):
            _ = functools.partial(func, *args, **kwargs)
            return await loop.run_in_executor(executor, _)

    return convert_to_async
