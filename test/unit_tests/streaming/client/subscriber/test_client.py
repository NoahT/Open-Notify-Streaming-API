from unittest import TestCase
from unittest.mock import MagicMock, patch

import redis

from src.streaming.client.subscriber.client import RedisSubscriberClient


class RedisSubscriberClientTestSuite(TestCase):

  def setUp(self):
    self._config = MagicMock()
    self._config.read_dict.return_value = {
        'HOST': 'localhost',
        'PORT': 6379,
        'CONNECT': {
            'TIMEOUT': 5.000
        },
        'SUBSCRIBE': {
            'SLEEP_TIME': 5.000
        },
        'CHANNEL': 'iss_location',
        'DECODE_RESPONSES': True
    }
    self._client = RedisSubscriberClient(config=self._config)

  @patch(target='redis.Redis')
  def test_should_subscribe_to_iss_channel_when_invoked(
      self, redis_patch: redis.Redis) -> None:
    pubsub_mock = MagicMock()

    redis_mock = MagicMock()
    redis_mock.pubsub.return_value = pubsub_mock

    redis_patch.return_value = redis_mock

    def handler(message):
      print('Placeholder handler')

    self._client.subscribe_iss_location(handler=handler)

    pubsub_mock.subscribe.assert_called()
