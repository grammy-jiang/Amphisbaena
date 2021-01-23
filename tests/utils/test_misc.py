"""
The test cases of miscellaneous
"""
import asyncio
import json
from unittest.case import TestCase
from unittest.main import main

from amphisbaena.settings import PRIORITIES, Settings
from amphisbaena.utils.misc import load_object, to_async, to_sync
from tests.samples import settings


class MiscTest(TestCase):
    """
    The test cases of miscellaneous
    """

    def test_load_object_class(self) -> None:
        """

        :return:
        :rtype: None
        """
        obj = load_object("amphisbaena.settings.Settings")  # class
        self.assertIs(obj, Settings)

    def test_load_object_func(self) -> None:
        """

        :return:
        :rtype: None
        """
        func = load_object("amphisbaena.utils.misc.load_object")  # func
        self.assertIs(func, load_object)

    def test_load_object_variable(self) -> None:
        """

        :return:
        :rtype: None
        """
        var = load_object("amphisbaena.settings.PRIORITIES")  # variable
        self.assertIs(var, PRIORITIES)

    def test_load_object_module(self) -> None:
        """

        :return:
        :rtype: None
        """
        module = load_object("tests.samples.settings")  # module
        self.assertIs(module, settings)

        module = load_object("json")  # module
        self.assertIs(module, json)

    def test_to_sync(self):
        @to_sync
        def sync_func(a, b, c=None):
            return a, b, c

        self.assertSequenceEqual(sync_func("a", "b", "c"), ("a", "b", "c"))

        @to_sync
        async def async_func(a, b, c=None):
            return a, b, c

        self.assertSequenceEqual(async_func("a", "b", "c"), ("a", "b", "c"))

    def test_to_async(self):
        loop = asyncio.get_event_loop()

        @to_async
        def sync_func(a, b, c=None):
            return a, b, c

        self.assertSequenceEqual(
            loop.run_until_complete(sync_func("a", "b", "c")), ("a", "b", "c")
        )

        @to_async
        async def async_func(a, b, c=None):
            return a, b, c

        self.assertSequenceEqual(
            loop.run_until_complete(async_func("a", "b", "c")), ("a", "b", "c")
        )


if __name__ == "__main__":
    main()
