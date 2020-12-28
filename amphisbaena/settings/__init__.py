"""
Settings
"""

from __future__ import annotations

from collections.abc import MutableMapping
from contextlib import contextmanager
from dataclasses import dataclass
from importlib import import_module
from types import ModuleType
from typing import Any, Dict, Generator, Iterator, Mapping, Union

# The pair of priority and priority_value
PRIORITIES: Dict[str, int] = {
    "default": 0,
    "project": 20,
    "env": 40,
    "cmd": 60,
}


@dataclass
class Setting:
    """
    The single setting container
    """

    priority: str
    value: Any

    def __post_init__(self):
        self.priority_value = PRIORITIES[self.priority]


class SettingsException(Exception):
    """
    The base exception
    """


class SettingsFrozenException(SettingsException):
    """
    The exception when modify a frozen settings instance
    """


class SettingsLowPriorityException(SettingsException):
    """
    The exception when modify a setting with a lower priority
    """


class BaseSettings(MutableMapping):
    """
    base settings class
    """

    class FrozenCheck:  # pylint: disable = too-few-public-methods
        """
        A decorator for Settings frozen status check
        """

        def __call__(self, method):
            def frozen_check(settings: BaseSettings, *args, **kwargs):
                if settings.is_frozen():
                    raise SettingsFrozenException
                return method(settings, *args, **kwargs)

            return frozen_check

    frozen_check = FrozenCheck()

    def __init__(self, settings: Mapping = None, priority: str = "project"):
        """

        :param settings:
        :type settings: Mapping
        :param priority:
        :type priority: str
        """
        self._priority = priority

        self._data: Dict[str, Setting] = {}

        self._frozen: bool = False

        if settings:
            self.update(settings)

        self._frozen = True

    def is_frozen(self) -> bool:
        """
        check this settings class frozen or not
        :return:
        """
        return self._frozen

    @contextmanager
    def unfreeze(self, priority: str = "project") -> Generator:
        """
        A context manager to unfreeze this instance and keep the previous frozen
        status
        """
        _priority: str
        _priority, self._priority = self._priority, priority

        status: bool
        status, self._frozen = self._frozen, False

        try:
            yield self
        finally:
            self._priority = _priority
            self._frozen = status

    # ---- abstract methods of MutableMapping ---------------------------------

    @frozen_check
    def __setitem__(self, k: str, v: Any) -> None:
        """

        :param k:
        :type k: str
        :param v:
        :type v: Any
        :return:
        :rtype: None
        """
        setting: Setting = Setting(priority=self._priority, value=v)
        if k in self:
            _v = self._data[k]
            if PRIORITIES[self._priority] < _v.priority_value:
                raise SettingsLowPriorityException

        self._data[k] = setting

    @frozen_check
    def __delitem__(self, k: str) -> None:
        """

        :param k:
        :type k: str
        :return:
        :rtype: None
        """
        del self._data[k]

    def __getitem__(self, k: str) -> Any:
        """

        :param k:
        :type k: str
        :return:
        :rtype: Any
        """
        return self._data[k].value

    def __len__(self) -> int:
        """

        :return:
        :rtype: int
        """
        return len(self._data)

    def __iter__(self) -> Iterator[str]:
        """

        :return:
        :rtype: Iterator[str]
        """
        return iter(self._data)

    def __contains__(self, k: str) -> bool:  # type: ignore
        """

        :param k:
        :type k: str
        :return:
        :rtype: bool
        """
        return k in self._data


class Settings(BaseSettings):  # pylint: disable=too-many-ancestors
    """
    settings class
    """

    def __init__(
        self,
        settings: Mapping = None,
        priority: str = "project",
        load_default: bool = True,
    ):
        """

        :param settings:
        :type settings: Mapping
        :param priority:
        :type priority: str
        :param load_default:
        :type load_default: bool
        """
        super().__init__(settings, priority)

        if load_default:
            with self.unfreeze(priority="default") as settings_:
                settings_.load_module(  # pylint: disable=no-member
                    f"{self.__module__}.default_settings"
                )

    def load_module(self, module: Union[ModuleType, str]) -> None:
        """

        :param module:
        :type module: Union[ModuleType, str]
        :return:
        :rtype: None
        """
        if isinstance(module, str):
            module = import_module(module)

        for key in dir(module):
            if key.isupper():
                self[key] = getattr(module, key)

    def copy_to_dict(self) -> Dict[str, Any]:
        """

        :return:
        :rtype: Dict[str, Any]
        """
        return dict(self.items())
