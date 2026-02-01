''' Integration test module for ISS data storage. '''
import time
import unittest
from test.integration_tests.streaming.config import config

from iss_location_client.client import ISSLocationFirestoreClient
from iss_location_client.iss_location import ISSLocation


class ISSLocationFirestoreClientTestSuite(unittest.TestCase):
  '''
  Integration test suite for ISSLocationFirestoreClient.
  '''

  @classmethod
  def setUpClass(cls) -> None:
    cls._client = ISSLocationFirestoreClient(config=config,
                                             collection_name='iss_locations_it')

  @classmethod
  def tearDownClass(cls):
    return super().tearDownClass()

  def test_should_get_iss_location_documents_correctly(self) -> None:
    iss_location_obj1 = ISSLocation(ts=int(time.time()),
                                    pos_la=1.2345,
                                    pos_lo=6.7890)
    self._client.add_iss_location(iss_location=iss_location_obj1)
    iss_location_obj2 = ISSLocation(ts=int(time.time()),
                                    pos_la=2.3456,
                                    pos_lo=7.8901)
    self._client.add_iss_location(iss_location=iss_location_obj2)

    ts_to = int(time.time())
    ts_from = ts_to - 10
    iss_location_documents = self._client.get_iss_locations(ts_from=ts_from,
                                                            ts_to=ts_to)

    self.assertIsNotNone(iss_location_documents)
    self.assertTrue(
        any(document == iss_location_obj1
            for document in iss_location_documents))
    self.assertTrue(
        any(document == iss_location_obj2
            for document in iss_location_documents))
