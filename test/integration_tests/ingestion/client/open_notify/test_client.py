''' Integration test module for Open Notify client. '''
import unittest
from test.integration_tests.ingestion.config import config

from src.ingestion.client.open_notify.client import (
    FaultTolerantOpenNotifyRequestsClient, OpenNotifyRequestsClient)


class OpenNotifyRequestsClientTestSuite(unittest.TestCase):
  '''
  Integration test suite for OpenNotifyRequestsClient.
  '''

  def setUp(self) -> None:
    self._client = OpenNotifyRequestsClient(config=config)

  def test_should_return_iss_data_on_successful_request(self) -> None:
    response = self._client.get_iss()

    self.assertIsNotNone(response)
    self.assertIsNotNone(response['timestamp'])
    self.assertEqual('success', response['message'])
    self.assertIsNotNone(response['iss_position'])
    self.assertIsNotNone(response['iss_position']['latitude'])
    self.assertIsNotNone(response['iss_position']['longitude'])


class FaultTolerantOpenNotifyRequestsClientTestSuite(
    OpenNotifyRequestsClientTestSuite):
  '''
  Integration test suite for FaultTolerantOpenNotifyRequestsClient.
  '''

  def setUp(self) -> None:
    self._client = FaultTolerantOpenNotifyRequestsClient(
        client=OpenNotifyRequestsClient(config=config))
