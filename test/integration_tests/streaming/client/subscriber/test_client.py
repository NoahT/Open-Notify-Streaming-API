''' Module for integration testing SubscriberClient implementations. '''
import logging
import time
from test.integration_tests.streaming.config import config
from unittest import TestCase

from iss_location_client.iss_location import ISSLocation

from src.ingestion.client.publisher.client import RedisPublisherClient
from src.streaming.client.subscriber.client import RedisSubscriberClient


class RedisSubscriberClientTestSuite(TestCase):
  '''
  Integration test suite for RedisSubscriberClient.
  '''

  def setUp(self):
    self._config = config
    self._client_subscriber = RedisSubscriberClient(config=self._config)
    self._client_publisher = RedisPublisherClient(config=self._config)

  def test_should_correctly_consume_messages_from_iss_channel(self) -> None:
    self._is_consumed = False

    def handler(message):
      logging.warning('Message consumed: %s', message['data'])
      self._is_consumed = True

    self._client_subscriber.subscribe_iss_location(handler=handler)

    iss_location = ISSLocation.from_dict({
        'ts': int(time.time()),
        'pos_la': 1.2345,
        'pos_lo': 6.7890
    })
    self._client_publisher.publish_iss_location(iss_location=iss_location)

    time.sleep(5)

    self.assertTrue(self._is_consumed)

  def tearDown(self):
    self._client_subscriber.close_channel()
