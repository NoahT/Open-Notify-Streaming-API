''' Integration test module for ISS data storage. '''
import time
import unittest
from test.integration_tests.streaming import (iss_client, iss_location1,
                                              iss_location2)


class ISSLocationFirestoreClientTestSuite(unittest.TestCase):
  '''
  Integration test suite for ISSLocationFirestoreClient.
  '''

  def setUp(self):
    self._client = iss_client

  @classmethod
  def tearDownClass(cls):
    return super().tearDownClass()

  def test_should_get_iss_location_documents_correctly(self) -> None:
    ts_to = int(time.time())
    ts_from = ts_to - 40
    iss_location_documents = self._client.get_iss_locations(ts_from=ts_from,
                                                            ts_to=ts_to)

    self.assertIsNotNone(iss_location_documents)
    self.assertTrue(
        any(document == iss_location1 for document in iss_location_documents))
    self.assertTrue(
        any(document == iss_location2 for document in iss_location_documents))
