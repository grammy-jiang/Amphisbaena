"""
The test cases of log
"""
import logging
from unittest.case import TestCase
from unittest.main import main
from unittest.mock import MagicMock, patch

from amphisbaena.settings import Settings
from amphisbaena.utils.log import configure_logging, get_runtime_info


class LogTest(TestCase):
    """
    The test cases of log
    """

    @patch("logging.root.addHandler")
    def test_configure_logging(self, add_handler: MagicMock) -> None:
        """

        :param add_handler:
        :type add_handler: MagicMock
        :return:
        :rtype: None
        """
        settings = Settings(default_settings=True)
        configure_logging(settings)

        add_handler.assert_called()
        (handler,), _ = add_handler.call_args
        self.assertIsInstance(handler, logging.StreamHandler)

        self.assertEqual(handler.level, settings["LOG_LEVEL"])
        self.assertEqual(handler.formatter.datefmt, settings["LOG_FORMATTER_DATEFMT"])
        self.assertEqual(handler.formatter._fmt, settings["LOG_FORMATTER_FMT"])

    def test_get_runtime_info(self) -> None:
        """

        :return:
        :rtype: None
        """
        logger = logging.getLogger("test")
        with self.assertLogs("test", level=logging.INFO) as logs_cm:
            get_runtime_info(logger)

        self.assertSequenceEqual(
            [x.msg for x in logs_cm.records],
            [
                "Platform: %(platform)s",
                "Platform details:\n%(details)s",
                "Versions:\n%(versions)s",
            ],
        )


if __name__ == "__main__":
    main()
