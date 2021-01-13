"""
The main of the module
"""
import logging
import sys
from argparse import Action, ArgumentParser, Namespace
from typing import Dict
from ast import literal_eval

import amphisbaena
from amphisbaena.settings import Settings
from amphisbaena.utils import configure_logging, get_runtime_info


class SettingsAppend(Action):  # pylint: disable=too-few-public-methods
    """
    Save settings into dict
    """

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: str,
        option_string=None,
    ) -> None:
        """

        :param parser:
        :param namespace:
        :param values:
        :param option_string:
        :return:
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
    parser = ArgumentParser()

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


def main():
    args: Namespace = get_arguments(*sys.argv[1:])

    settings = Settings(settings=args.settings, priority="cmd", default_settings=True)
    set_logging(settings)


if __name__ == "__main__":
    main()
