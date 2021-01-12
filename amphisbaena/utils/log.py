"""
logging functions
"""
import logging
import platform
import pprint
import ssl

import orjson
import yaml

from amphisbaena.settings import Settings


def configure_logging(settings: Settings) -> None:
    """

    :param settings:
    :type settings: Settings
    :return:
    :rtype: None
    """
    # Get a console handler and configure it
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        fmt=settings["LOG_FORMATTER_FMT"],
        datefmt=settings["LOG_FORMATTER_DATEFMT"],
    )
    console_handler.setFormatter(formatter)
    console_handler.setLevel(settings["LOG_LEVEL"])

    # add this console handler into logging
    logging.root.addHandler(console_handler)


def get_runtime_info(logger) -> None:
    """

    :param logger:
    :type logger: logging.Logger
    :return:
    :rtype: None
    """
    logger.info(
        "Platform: %(platform)s", {"platform": pprint.pformat(platform.platform())}
    )

    logger.info(
        "Platform details:\n%(details)s",
        {
            "details": pprint.pformat(
                {
                    "OpenSSL": ssl.OPENSSL_VERSION,
                    "architecture": platform.architecture(),
                    "machine": platform.machine(),
                    "node": platform.node(),
                    "processor": platform.processor(),
                    "python_build": platform.python_build(),
                    "python_compiler": platform.python_compiler(),
                    "python_branch": platform.python_branch(),
                    "python_implementation": platform.python_implementation(),
                    "python_revision": platform.python_revision(),
                    "python_version": platform.python_version(),
                    "release": platform.release(),
                    "system": platform.system(),
                    "version": platform.version(),
                }
            )
        },
    )

    logger.info(
        "Versions:\n%(versions)s",
        {
            "versions": pprint.pformat(
                {
                    "Python": platform.python_version(),
                    "orjson": orjson.__version__,
                    "PyYAML": yaml.__version__,
                }
            )
        },
    )
