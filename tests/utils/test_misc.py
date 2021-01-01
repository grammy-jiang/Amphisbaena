"""
The test cases of miscellaneous
"""
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
        obj = load_object("amphisbaena.settings.Settings")
        self.assertIs(obj, Settings)

        func = load_object("amphisbaena.utils.misc.load_object", type_="function")
        self.assertIs(func, load_object)

        var = load_object("amphisbaena.settings.PRIORITIES", type_="variable")
        self.assertIs(var, PRIORITIES)

    def test_load_object_module(self) -> None:
        """

        :return:
        :rtype: None
        """
        module = load_object("tests.samples.settings", type_="module")

        self.assertIs(module, settings)


if __name__ == "__main__":
    main()
