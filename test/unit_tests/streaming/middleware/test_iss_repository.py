'''
  Module containing unit tests for ISSRepository 
  implementations.
'''
from unittest import TestCase
from unittest.mock import MagicMock

from iss_location_client.iss_location import ISSLocation

from src.streaming.middleware.iss_repository import ISSPassThroughRepository


class ISSPassThroughRepositoryTestSuite(TestCase):
  ''' Unit test suite for ISSPassThroughRepository '''

  def setUp(self) -> None:
    self._client = MagicMock()
    self._repository = ISSPassThroughRepository(client=self._client)

  def test_should_pass_through_results_from_iss_client(self) -> None:
    iss_location1 = ISSLocation.from_dict({
        'ts': 123,
        'pos_la': 4.56,
        'pos_lo': 7.89
    })
    iss_location2 = ISSLocation.from_dict({
        'ts': 456,
        'pos_la': 7.89,
        'pos_lo': 0.12
    })
    iss_locations = [iss_location1, iss_location2]
    self._client.get_iss_locations.return_value = iss_locations

    result = self._repository.get_iss_locations(10)

    self.assertEqual(iss_locations, result)
