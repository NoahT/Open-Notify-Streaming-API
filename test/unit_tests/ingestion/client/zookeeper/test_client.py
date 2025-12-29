"""
Test suite for Zookeeper client.
"""

import unittest
from unittest.mock import MagicMock

from kazoo.client import KazooClient

from src.ingestion.client.zookeeper.client import KazooZookeeperClient


class KazooZookeeperClientTestSuite(unittest.TestCase):
  """Test suite for KazooZookeeperClient."""

  def setUp(self):
    self._kazoo_client = MagicMock(spec=KazooClient)
    self._kazoo_client.logger = MagicMock()
    self._kazoo_zookeeper_client = KazooZookeeperClient(self._kazoo_client)

  def test_should_delegate_start_to_kazoo_client(self) -> None:
    self._kazoo_zookeeper_client.start()

    self._kazoo_client.start.assert_called()

  def test_should_delegate_stop_to_kazoo_client(self) -> None:
    self._kazoo_zookeeper_client.stop()

    self._kazoo_client.stop.assert_called()

  def test_should_delegate_listener_to_kazoo_client(self) -> None:

    def listener(_):
      pass

    self._kazoo_zookeeper_client.add_listener(listener)

    self._kazoo_client.add_listener.assert_called_with(listener)

  def test_should_not_delegate_create_if_path_exists(self) -> None:
    self._kazoo_client.exists.return_value = MagicMock()
    self._kazoo_zookeeper_client.create('/path', b'value')

    self._kazoo_client.create.assert_not_called()

  def test_should_delegate_create_if_path_exists(self) -> None:
    self._kazoo_client.exists.return_value = None
    self._kazoo_zookeeper_client.create('/path', b'value')

    self._kazoo_client.create.assert_called()

  def test_should_delegate_set_to_kazoo_client(self) -> None:
    self._kazoo_zookeeper_client.set('/path', b'value')

    self._kazoo_client.set.assert_called_with('/path', b'value')

  def test_should_delegate_get_to_kazoo_client(self) -> None:
    self._kazoo_zookeeper_client.get('/path')

    self._kazoo_client.get.assert_called_with('/path', watch=None)

  def test_should_delegate_get_children_to_kazoo_client(self) -> None:
    self._kazoo_zookeeper_client.get_children('/path')

    self._kazoo_client.get_children.assert_called_with('/path')
