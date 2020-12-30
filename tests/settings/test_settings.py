"""
Test BaseSettings class
"""
from collections.abc import Iterable
from types import ModuleType
from unittest.case import TestCase
from unittest.main import main

from amphisbaena.settings import (
    PRIORITIES,
    BaseSettings,
    CompareWithNotSameNameSettingException,
    CompareWithNotSettingException,
    Setting,
    Settings,
    SettingsFrozenException,
    SettingsLowOrEqualPriorityException,
)


class SettingTest(TestCase):
    """
    The test case for Setting
    """

    def setUp(self) -> None:
        """

        :return:
        :rtype: None
        """
        self.setting_a = Setting("default", "a", "a")
        self.setting_b = Setting("project", "b", "b")
        self.setting_c = Setting("env", "c", "c")
        self.setting_d = Setting("cmd", "d", "d")

    def tearDown(self) -> None:
        """

        :return:
        :rtype: None
        """
        del self.setting_a
        del self.setting_b
        del self.setting_c
        del self.setting_d

    def test_priority_value(self) -> None:
        """

        :return:
        :rtype: None
        """
        self.assertEqual(self.setting_a.priority_value, PRIORITIES["default"])
        self.assertEqual(self.setting_b.priority_value, PRIORITIES["project"])
        self.assertEqual(self.setting_c.priority_value, PRIORITIES["env"])
        self.assertEqual(self.setting_d.priority_value, PRIORITIES["cmd"])

    def test_eq(self) -> None:
        """

        :return:
        :rtype: None
        """
        with self.assertRaises(CompareWithNotSettingException):
            self.assertTrue("a_false_setting" == self.setting_a)

        setting_equal = Setting("default", "a", "a")
        self.assertTrue(setting_equal == self.setting_a)

        setting_not_same_priority = Setting("project", "a", "a")
        self.assertFalse(setting_not_same_priority == self.setting_a)

        setting_not_same_name = Setting("default", "not_same_name", "a")
        self.assertFalse(setting_not_same_name == self.setting_a)

        setting_not_same_value = Setting("default", "a", "not_same_value")
        self.assertFalse(setting_not_same_value == self.setting_a)

    def test_ne(self) -> None:
        """

        :return:
        :rtype: None
        """
        with self.assertRaises(CompareWithNotSettingException):
            self.assertTrue("a_false_setting" != self.setting_a)

        setting_not_same_priority = Setting("project", "a", "a")
        self.assertTrue(setting_not_same_priority != self.setting_a)

        setting_not_same_name = Setting("default", "not_same_name", "a")
        self.assertTrue(setting_not_same_name != self.setting_a)

        setting_not_same_value = Setting("default", "a", "not_same_value")
        self.assertTrue(setting_not_same_value != self.setting_a)

        setting_equal = Setting("default", "a", "a")
        self.assertFalse(setting_equal != self.setting_a)

    def test_lt(self) -> None:
        """

        :return:
        :rtype: None
        """
        with self.assertRaises(CompareWithNotSettingException):
            self.assertTrue(self.setting_a < "a_false_setting")

        with self.assertRaises(CompareWithNotSameNameSettingException):
            setting_not_same_name = Setting("default", "not_same_name", "a")
            self.assertTrue(setting_not_same_name < self.setting_a)

        setting_b_lt = Setting("default", "b", "b")
        self.assertTrue(setting_b_lt < self.setting_b)

        setting_b_not_lt = Setting("project", "b", "b")
        self.assertFalse(setting_b_not_lt < self.setting_b)

        setting_b_not_lt = Setting("env", "b", "b")
        self.assertFalse(setting_b_not_lt < self.setting_b)

    def test_gt(self) -> None:
        """

        :return:
        :rtype: None
        """
        with self.assertRaises(CompareWithNotSettingException):
            self.assertTrue("a_false_setting" > self.setting_a)

        with self.assertRaises(CompareWithNotSameNameSettingException):
            setting_not_same_name = Setting("default", "not_same_name", "a")
            self.assertTrue(setting_not_same_name > self.setting_a)

        setting_b_gt = Setting("env", "b", "b")
        self.assertTrue(setting_b_gt > self.setting_b)

        setting_b_not_gt = Setting("project", "b", "b")
        self.assertFalse(setting_b_not_gt > self.setting_b)

        setting_b_not_gt = Setting("default", "b", "b")
        self.assertFalse(setting_b_not_gt > self.setting_b)

    def test_le(self) -> None:
        """

        :return:
        :rtype: None
        """
        with self.assertRaises(CompareWithNotSettingException):
            self.assertTrue(self.setting_a <= "a_false_setting")

        with self.assertRaises(CompareWithNotSameNameSettingException):
            setting_not_same_name = Setting("default", "not_same_name", "a")
            self.assertTrue(setting_not_same_name <= self.setting_a)

        setting_b_le = Setting("default", "b", "b")
        self.assertTrue(setting_b_le <= self.setting_b)

        setting_b_le = Setting("project", "b", "b")
        self.assertTrue(setting_b_le <= self.setting_b)

        setting_b_not_le = Setting("env", "b", "b")
        self.assertFalse(setting_b_not_le <= self.setting_b)

    def test_ge(self) -> None:
        """

        :return:
        :rtype: None
        """
        with self.assertRaises(CompareWithNotSettingException):
            self.assertTrue("a_false_setting" >= self.setting_a)

        with self.assertRaises(CompareWithNotSameNameSettingException):
            setting_not_same_name = Setting("default", "not_same_name", "a")
            self.assertTrue(setting_not_same_name >= self.setting_a)

        setting_b_ge = Setting("project", "b", "b")
        self.assertTrue(setting_b_ge >= self.setting_b)

        setting_b_ge = Setting("env", "b", "b")
        self.assertTrue(setting_b_ge >= self.setting_b)

        setting_b_not_ge = Setting("default", "b", "b")
        self.assertFalse(setting_b_not_ge >= self.setting_b)


class BaseSettingsTest(TestCase):
    """
    test BaseSettings class
    """

    def test_init(self) -> None:
        """
        test the initialize method
        :return:
        :rtype: None
        """

        settings = BaseSettings()
        self.assertDictEqual(settings._data, {})  # pylint: disable = protected-access

        settings = BaseSettings(settings={"a": 1, "b": 2})
        self.assertDictEqual(
            settings._data,  # pylint: disable = protected-access
            {
                "a": Setting("project", "a", 1),
                "b": Setting("project", "b", 2),
            },
        )

        self.assertTrue(settings.is_frozen())
        self.assertEqual(
            settings._priority, "project"  # pylint: disable = protected-access
        )

    def test_is_frozen(self) -> None:
        """
        test the method is_frozen
        :return:
        :rtype: None
        """

        settings = BaseSettings()
        self.assertTrue(settings.is_frozen())

        with settings.unfreeze() as settings_:
            self.assertFalse(settings_.is_frozen())

    def test_unfreeze(self) -> None:
        """
        test the context manager unfreeze
        :return:
        :rtype: None
        """

        settings = BaseSettings()
        self.assertTrue(settings.is_frozen())
        with settings.unfreeze() as settings_:
            self.assertFalse(settings_.is_frozen())
        self.assertEqual(
            settings._priority,  # pylint: disable = protected-access
            "project",
        )

        with settings.unfreeze(priority="user") as settings_:
            self.assertFalse(settings_.is_frozen())
            self.assertEqual(
                settings_._priority, "user"  # pylint: disable = protected-access
            )
        self.assertEqual(
            settings._priority, "project"  # pylint: disable = protected-access
        )

    def test_setitem(self):
        """
        test the method of setitem
        :return:
        """
        settings = BaseSettings(settings={"a": 1, "b": 2})
        with settings.unfreeze() as settings_:
            settings_["c"] = 3
        self.assertEqual(settings["c"], 3)

        with self.assertRaises(SettingsFrozenException):
            settings["c"] = 3

        with self.assertRaises(SettingsLowOrEqualPriorityException):
            with settings.unfreeze("default") as settings_:
                settings_["a"] = 3

        with self.assertRaises(SettingsLowOrEqualPriorityException):
            with settings.unfreeze("project") as settings_:
                settings_["a"] = 3

    def test_delitem(self):
        """
        test the method of del
        :return:
        """
        settings = BaseSettings(settings={"a": 1, "b": 2})
        with settings.unfreeze() as settings_:
            del settings_["a"]
        self.assertNotIn("a", settings)

        with self.assertRaises(SettingsFrozenException):
            del settings["a"]

    def test_getitem(self):
        """
        test the method of getitem
        :return:
        """
        settings = BaseSettings(settings={"a": 1, "b": 2})
        self.assertEqual(settings["a"], 1)

    def test_len(self):
        """
        test the method of len
        :return:
        """
        settings = BaseSettings(settings={"a": 1, "b": 2})
        self.assertEqual(len(settings), 2)

        settings = BaseSettings()
        self.assertEqual(len(settings), 0)

    def test_iter(self):
        """
        test the method of iter
        :return:
        """
        settings = BaseSettings()
        self.assertIsInstance(settings, Iterable)

    def test_contains(self):
        """
        test the method of contains
        :return:
        """
        settings = BaseSettings(settings={"a": 1, "b": 2})
        self.assertTrue("a" in settings)
        self.assertFalse("c" in settings)


class SettingsTest(TestCase):
    """
    test Settings class
    """

    def setUp(self) -> None:
        """

        :return:
        :rtype: None
        """
        self.test_module = ModuleType(name="test")
        setattr(self.test_module, "A", 1)

    def tearDown(self) -> None:
        """

        :return:
        :rtype: None
        """
        del self.test_module

    def test_update_from_module(self):
        """
        test the method of update_from_module
        :return:
        """

        settings = Settings()
        settings_: Settings
        with settings.unfreeze() as settings_:
            settings_.load_module(self.test_module)  # pylint: disable=no-member

        self.assertIn("A", settings)
        self.assertEqual(
            settings._data["A"],  # pylint: disable = protected-access
            Setting("project", "A", 1),
        )

        # settings = Settings()
        # settings_: Settings
        # with settings.unfreeze() as settings_:
        #     settings_.load_module(  # pylint: disable=no-member
        #         "amphisbaena.settings.default"
        #     )

        # self.assertIn("LOG_LEVEL", settings)
        # self.assertEqual(
        #     settings._data["LOG_LEVEL"],  # pylint: disable = protected-access
        #     Setting(priority="project", priority_value=20, value=logging.INFO),
        # )

    def test_copy_to_dict(self):
        """

        :return:
        """
        settings = Settings(settings={"A": 1, "B": 2}, load_default=False)

        self.assertDictEqual(settings.copy_to_dict(), {"A": 1, "B": 2})


if __name__ == "__main__":
    main()
