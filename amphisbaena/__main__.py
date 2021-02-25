"""
The main of the module
"""
import logging
import os
import sys
from argparse import Action, ArgumentParser, Namespace
from ast import literal_eval
from typing import Dict

import orjson
import yaml

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


class ConfigAppend(Action):  # pylint: disable=too-few-public-methods
    """
    Load the config file into dict
    """

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: str,
        option_string=None,
    ):
        """

        :param parser:
        :param namespace:
        :param values:
        :param option_string:
        :return:
        """
        items: Dict = getattr(namespace, self.dest)

        suffix = values.rsplit(".")[-1]

        with open(values, "r") as config_fh:
            if suffix == "json":
                config = orjson.loads(config_fh.read())
            elif suffix in ("yaml", "yml"):
                config = yaml.safe_load(config_fh)

        items.update(config)

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
        "-c",
        "--config",
        action=ConfigAppend,
        default=dict(),
        help="load the configuration of the setting from a file",
    )
    parser.add_argument(
        "-s",
        "--setting",
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
    ns_args: Namespace = get_arguments(*args)

    settings = Settings(
        settings={**ns_args.setting, **ns_args.config},
        priority="cmd",
        default_settings=True,
    )
    set_logging(settings)


def entrypoint(*args):
    """

    :param args:
    :return:
    """
    if not args:
        args = sys.argv[1:]

    try:
        main(*args)
    except SettingsException:
        sys.exit(os.EX_CONFIG)
    else:
        sys.exit(os.EX_OK)


if __name__ == "__main__":
    entrypoint(*sys.argv[1:])
