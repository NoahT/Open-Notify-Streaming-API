''' Integration test module for ISS data storage. '''
import time
import unittest

from cfg_environ.config import ConfigFacade
from iss_location_client.client import ISSLocationFirestoreClient
from iss_location_client.iss_location import ISSLocation


class ISSLocationFirestoreClientTestSuite(unittest.TestCase):
  '''
  Integration test suite for ISSLocationFirestoreClient.
  '''

  @classmethod
  def setUpClass(cls) -> None:
    cls._config = ConfigFacade(
        'test/integration_tests/ingestion/client/iss_location', 'test',
        'default')
    cls._client = ISSLocationFirestoreClient(config=cls._config,
                                             collection_name='iss_locations_it')

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
