import time
import unittest

from src.ingestion.client.iss_location.client import ISSLocationFirestoreClient
from src.ingestion.client.iss_location.iss_location import ISSLocation
from src.ingestion.config.config_facade import ConfigFacade


class ISSLocationFirestoreClientTestSuite(unittest.TestCase):
  '''
  Integration test suite for ISSLocationFirestoreClient.
  '''

  @classmethod
  def setUpClass(self) -> None:
    # Same database; I really just didn't want to move out of free tier.
    # In the future wemight consider installing the Firestore emulator and
    # ITs with Docker compose so we can run the integration tests in a more
    # isolated manner.
    self._config = ConfigFacade(
        'test/integration_tests/ingestion/client/iss_location', 'test',
        'default')
    self._client = ISSLocationFirestoreClient(
        config=self._config, collection_name='iss_locations_it')

  @classmethod
  def tearDownClass(cls):
    return super().tearDownClass()

  def test_should_add_iss_location_documents_correctly(self) -> None:
    iss_location_obj = ISSLocation(ts=int(time.time()),
                                   pos_la=1.2345,
                                   pos_lo=6.7890)
    iss_location_document = self._client.add_iss_location(
        iss_location=iss_location_obj)

    self.assertIsNotNone(iss_location_document)

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
    # Rough window. Could fail due to concurrent runs. Again, can be fixed
    # in future if emulator inside container is used for integration tests.
    iss_location_documents = self._client.get_iss_locations(ts_from=ts_from,
                                                            ts_to=ts_to)

    self.assertIsNotNone(iss_location_documents)
    self.assertTrue(
        any(document == iss_location_obj1
            for document in iss_location_documents))
    self.assertTrue(
        any(document == iss_location_obj2
            for document in iss_location_documents))
