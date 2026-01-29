''' Module for testing ISSController implementations '''

from unittest import TestCase
from unittest.mock import MagicMock

from cfg_environ.config import Config
from iss_location_client.iss_location import ISSLocation
from werkzeug.exceptions import HTTPException

from src.streaming.middleware.iss_controller import V1ISSController
from src.streaming.middleware.iss_repository import ISSRepository


class V1ISSControllerTestSuite(TestCase):
  '''
  Unit test suite for V1ISSController
  '''

  def setUp(self):
    self._repository = MagicMock(spec=ISSRepository)
    self._repository_return_value = [
        ISSLocation.from_dict({
            'ts': 123,
            'pos_la': 4.56,
            'pos_lo': 7.89
        })
    ]
    # pylint:disable=line-too-long
    self._repository.get_iss_locations.return_value = self._repository_return_value
    self._config = MagicMock(spec=Config)
    self._config.read_dict.return_value = {
        'V1_ISS_EVENTS': {
            'PARAMS': {
                'WINDOW': {
                    'MINIMUM_VALUE': 10,
                    'MAXIMUM_VALUE': 600
                }
            }
        }
    }
    self._controller = V1ISSController(repository=self._repository,
                                       config=self._config)

  def test_should_return_repository_results_on_valid_request(self) -> None:
    result = self._controller.v1_iss_events(window=30)

    self.assertEqual(self._repository_return_value, result)

  def test_should_raise_exception_when_window_too_small(self) -> None:
    self.assertRaises(HTTPException, self._controller.v1_iss_events, window=9)

  def test_should_raise_exception_when_window_too_large(self) -> None:
    self.assertRaises(HTTPException, self._controller.v1_iss_events, window=601)
