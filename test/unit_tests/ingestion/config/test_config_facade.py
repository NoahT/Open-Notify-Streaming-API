""" Unit test module for config_facade. """
import unittest

from src.ingestion.config.config_facade import ConfigFacade


class ConfigFacadeTestSuite(unittest.TestCase):
  """ Unit test suite for ConfigFacade. """

  def setUp(self) -> None:
    self._config_facade = ConfigFacade('test/unit_tests/ingestion/config',
                                       'development', 'default')

  def test_should_return_str_in_config(self) -> None:
    value = self._config_facade.read_str('SOME_KEY_FOR_STR')
    self.assertEqual('some value', value)

  def test_should_return_bool_in_config(self) -> None:
    value = self._config_facade.read_bool('SOME_KEY_FOR_BOOL')
    self.assertTrue(value)

  def test_should_return_list_in_config(self) -> None:
    value = self._config_facade.read_list('SOME_KEY_FOR_LIST')
    self.assertEqual([1, 2, 3], value)

  def test_should_return_dict_in_config(self) -> None:
    value = self._config_facade.read_dict('SOME_KEY_FOR_DICT')
    self.assertEqual({'SOME_KEY_FOR_STR': 'some value'}, value)

  def test_should_return_int_in_config(self) -> None:
    value = self._config_facade.read_int('SOME_KEY_FOR_INT')
    self.assertEqual(12345, value)

  def test_should_return_float_in_config(self) -> None:
    value = self._config_facade.read_float('SOME_KEY_FOR_FLOAT')
    self.assertEqual(1.2345, value)

  def test_should_return_overridden_value(self) -> None:
    value = self._config_facade.read_str('SOME_KEY_FOR_OVERRIDE')
    self.assertEqual('This value should be set', value)

  def test_should_return_default_for_null_value(self) -> None:
    value = self._config_facade.read_str('SOME_KEY_FOR_NONE', 'my_default')
    self.assertEqual('my_default', value)
