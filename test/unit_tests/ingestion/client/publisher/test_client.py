''' Unit test module for PublisherClient implementations.'''
from unittest import TestCase
from unittest.mock import MagicMock, patch

import redis
from cfg_environ.config import Config
from iss_location_client.iss_location import ISSLocation

from src.ingestion.client.publisher.client import RedisPublisherClient


class RedisPublisherClientTestSuite(TestCase):
  '''
  Unit test suite for RedisPublisherClient.
  '''

  def setUp(self):
    self._config = MagicMock(spec=Config)
    self._config.read_dict.return_value = {
        'HOST': 'localhost',
        'PORT': 6379,
        'CONNECT': {
            'TIMEOUT': 5.000
        },
        'PUBLISH': {
            'TIMEOUT': 5.000
        },
        'CHANNEL': 'iss_location',
        'DECODE_RESPONSES': True
    }
    self._client = RedisPublisherClient(config=self._config)

  @patch(target='redis.Redis')
  def test_should_return_true_when_iss_location_data_published_successfully(
      self, redis_patch: redis.Redis) -> None:
    redis_mock = MagicMock()
    redis_mock.publish.return_value = 1
    redis_patch.return_value = redis_mock

    iss_location = ISSLocation.from_dict({
        'ts': 123,
        'pos_la': 4.56,
        'pos_lo': 7.89
    })

    is_published = self._client.publish_iss_location(iss_location=iss_location)

    self.assertTrue(is_published)

  @patch(target='redis.Redis')
  def test_should_return_false_when_iss_location_data_published_unsuccessfully(
      self, redis_patch: redis.Redis) -> None:
    redis_mock = MagicMock()
    redis_mock.publish.side_effect = RuntimeError('Redis publisher error')
    redis_patch.return_value = redis_mock

    iss_location = ISSLocation.from_dict({
        'ts': 123,
        'pos_la': 4.56,
        'pos_lo': 7.89
    })

    is_published = self._client.publish_iss_location(iss_location=iss_location)

    self.assertFalse(is_published)
