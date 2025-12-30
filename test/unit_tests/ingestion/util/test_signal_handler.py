"""Unit tests for signal handler."""

import signal
import unittest
from unittest.mock import MagicMock

from src.ingestion.client.zookeeper.client import Client
from src.ingestion.util.signal_handler import ZooKeeperSignalHandler


class ZooKeeperSignalHandlerTestSuite(unittest.TestCase):
  """Test suite for ZooKeeperSignalHandler."""

  def setUp(self):
    self._zookeeper_client = MagicMock(spec=Client)
    self._zookeeper_signal_handler = ZooKeeperSignalHandler(
        zookeeper_client=self._zookeeper_client)

  def test_should_add_handler_for_correct_signals(self) -> None:
    sigterm_handler = signal.getsignal(signal.SIGTERM)
    sigint_handler = signal.getsignal(signal.SIGINT)

    expected_handler = self._zookeeper_signal_handler.handle_shutdown

    self.assertEqual(expected_handler, sigterm_handler)
    self.assertEqual(expected_handler, sigint_handler)

  def test_should_set_shutdown_event_on_handler(self) -> None:
    self._zookeeper_signal_handler.handle_shutdown(signal.SIGTERM, None)
    shutdown_event = self._zookeeper_signal_handler.shutdown_event

    self.assertTrue(shutdown_event.is_set())

  def test_should_close_zookeeper_server_on_handler(self) -> None:
    self._zookeeper_signal_handler.handle_shutdown(signal.SIGTERM, None)

    self._zookeeper_client.stop.assert_called_once()
