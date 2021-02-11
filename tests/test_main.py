"""
The test cases of __main__
"""
import logging
from argparse import Namespace
from tempfile import NamedTemporaryFile
from unittest.case import TestCase
from unittest.main import main
from unittest.mock import MagicMock, patch

import orjson
import yaml

from amphisbaena.__main__ import get_arguments
from amphisbaena.__main__ import main as a_main
from amphisbaena.__main__ import set_logging
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

        args = ("--setting", "A=1", "--setting", "B=2")

        ns = get_arguments(*args)
        self.assertIsInstance(ns, Namespace)
        self.assertDictEqual(ns.setting, {"A": 1, "B": 2})

        args = ("-s", "A=1", "-s", "B=2")

        ns = get_arguments(*args)
        self.assertIsInstance(ns, Namespace)
        self.assertDictEqual(ns.setting, {"A": 1, "B": 2})

        with NamedTemporaryFile(suffix=".json") as fp:
            fp.write(orjson.dumps({"A": 1, "B": 2}))
            fp.seek(0)
            ns = get_arguments("--config", fp.name)
            self.assertIsInstance(ns, Namespace)
            self.assertDictEqual(ns.config, {"A": 1, "B": 2})

        with NamedTemporaryFile(mode="w", suffix=".yaml") as fp:
            fp.write(yaml.safe_dump({"A": 1, "B": 2}))
            fp.seek(0)
            ns = get_arguments("--config", fp.name)
            self.assertIsInstance(ns, Namespace)
            self.assertDictEqual(ns.config, {"A": 1, "B": 2})

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

    @patch("amphisbaena.__main__.set_logging")
    def test_main(self, set_logging: MagicMock) -> None:
        """

        :param set_logging:
        :type set_logging: MagicMock
        :return:
        :rtype: None
        """
        a_main("--setting", "A=1", "-s", "B=2")

        set_logging.assert_called()
        (settings,) = set_logging.call_args[0]
        self.assertIn("A", settings)
        self.assertEqual(settings["A"], 1)
        self.assertIn("B", settings)
        self.assertEqual(settings["B"], 2)


if __name__ == "__main__":
    main()
