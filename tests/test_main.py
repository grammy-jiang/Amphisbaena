"""
The test cases of __main__
"""
from argparse import Namespace
from unittest.case import TestCase
from unittest.main import main

from amphisbaena.__main__ import get_arguments


class MainTest(TestCase):
    """
    The test cases of __main__
    """

    def test_get_arguments(self) -> None:
        """

        :return:
        :rtype: None
        """

        args = ("--settings", "a=1")

        ns = get_arguments(*args)
        self.assertIsInstance(ns, Namespace)
        self.assertDictEqual(ns.settings, {"a": 1})

        args = ("-s", "b=2")

        ns = get_arguments(*args)
        self.assertIsInstance(ns, Namespace)
        self.assertDictEqual(ns.settings, {"b": 2})


if __name__ == "__main__":
    main()
