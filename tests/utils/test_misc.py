"""
The test cases of miscellaneous
"""
import json
from unittest.case import TestCase
from unittest.main import main

from amphisbaena.settings import PRIORITIES, Settings
from amphisbaena.utils.misc import load_object
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


if __name__ == "__main__":
    main()
