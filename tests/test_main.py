"""
The test cases of __main__
"""
import logging
from argparse import Namespace
from unittest.case import TestCase
from unittest.main import main
from unittest.mock import MagicMock, patch

from amphisbaena.__main__ import get_arguments, set_logging
from amphisbaena.settings import Settings


class MainTest(TestCase):
    """
    The test cases of __main__
    """

    def test_get_arguments(self) -> None:
        """

        :return:
        :rtype: None
        """

        args = ("--settings", "a=1", "--settings", "b=2")

        ns = get_arguments(*args)
        self.assertIsInstance(ns, Namespace)
        self.assertDictEqual(ns.settings, {"a": 1, "b": 2})

        args = ("-s", "a=1", "-s", "b=2")

        ns = get_arguments(*args)
        self.assertIsInstance(ns, Namespace)
        self.assertDictEqual(ns.settings, {"a": 1, "b": 2})

    @patch("amphisbaena.__main__.configure_logging")
    @patch("amphisbaena.__main__.get_runtime_info")
    def test_set_logging(
        self, get_runtime_info: MagicMock, configure_logging: MagicMock
    ) -> None:
        """

        :param configure_logging:
        :type configure_logging: MagicMock
        :param get_runtime_info:
        :type get_runtime_info: MagicMock
        :return:
        :rtype: None
        """
        settings = Settings(default_settings="tests.samples.settings")
        set_logging(settings)

        logger = logging.getLogger("amphisbaena")

        configure_logging.assert_called_once_with(settings)
        get_runtime_info.assert_called_once_with(logger)
        self.assertEqual(logger.level, settings["LOG_LEVEL"])


if __name__ == "__main__":
    main()
