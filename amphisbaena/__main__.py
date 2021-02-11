"""
The main of the module
"""
import logging
import os
import sys
from argparse import Action, ArgumentParser, Namespace
from ast import literal_eval
from typing import Dict

import amphisbaena
from amphisbaena.settings import Settings, SettingsException
from amphisbaena.utils import configure_logging, get_runtime_info

PROG = "amphisbaena"


class SettingsAppend(Action):  # pylint: disable=too-few-public-methods
    """
    Save settings into dict
    """

    def __call__(  # type: ignore
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: str,
        option_string=None,
    ) -> None:
        """

        :param parser:
        :type parser: ArgumentParser
        :param namespace:
        :type namespace: Namespace
        :param values:
        :type values: str
        :param option_string:
        :type option_string:
        :return:
        :rtype: None
        """
        items: Dict = getattr(namespace, self.dest)

        key: str
        value: str
        key, value = values.split("=", 1)
        items.update({key: literal_eval(value)})

        setattr(namespace, self.dest, items)


def get_arguments(*args) -> Namespace:
    """

    :param args:
    :type args:
    :return:
    :rtype: Namespace
    """
    parser = ArgumentParser(prog=PROG)

    parser.add_argument(
        "-s",
        "--settings",
        action=SettingsAppend,
        default=dict(),
        help="configure the setting from command line interface",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="print the version number and exit (also --version)",
        version=f"%(prog)s {amphisbaena.__version__}",
    )

    return parser.parse_args(args)


def set_logging(settings: Settings) -> None:
    """

    :param settings:
    :type settings: Settings
    :return:
    :rtype: None
    """
    configure_logging(settings)

    logger = logging.getLogger("amphisbaena")
    logger.setLevel(settings["LOG_LEVEL"])

    get_runtime_info(logger)


def main(*args):
    """

    :param args:
    :return:
    """
    if not args:
        args = sys.argv[1:]

    ns_args: Namespace = get_arguments(*args)

    settings = Settings(
        settings=ns_args.settings, priority="cmd", default_settings=True
    )
    set_logging(settings)


if __name__ == "__main__":
    try:
        main(*sys.argv[1:])
    except SettingsException:
        sys.exit(os.EX_CONFIG)
    else:
        sys.exit(os.EX_OK)
