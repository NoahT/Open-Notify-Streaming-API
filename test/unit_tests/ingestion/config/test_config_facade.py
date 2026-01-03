""" Unit test module for config_facade. """
import unittest

from src.ingestion.config.config_facade import ConfigFacade


# pylint: disable=unused-argument
def env_util_side_effect(*args, **kwargs):
  return 'development'


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
