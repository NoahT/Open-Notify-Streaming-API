''' Integration test module for PublisherClient implementations. '''
import time
from unittest import TestCase

from src.ingestion.client.iss_location.iss_location import ISSLocation
from src.ingestion.client.publisher.client import RedisPublisherClient
from src.ingestion.config.config_facade import ConfigFacade


class RedisPublisherClientTestsuite(TestCase):
  '''
  Integration test suite for RedisPublisherClient.
  '''

  def setUp(self):
    self._config = ConfigFacade(
        config_path='test/integration_tests/ingestion/client/publisher',
        config_env='test',
        config_env_default='default')
    self._client = RedisPublisherClient(config=self._config)

  def test_should_successfully_publish_iss_location_to_redis_server(
      self) -> None:
    iss_location = ISSLocation.from_dict({
        'ts': int(time.time()),
        'pos_la': 1.234567,
        'pos_lo': 8.901234
    })

    is_published = self._client.publish_iss_location(iss_location=iss_location)

    self.assertTrue(is_published)
