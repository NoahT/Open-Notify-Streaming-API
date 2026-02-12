''' Init module for signal handling. '''

from ..client.zookeeper.client import Client
from .signal_handler import SignalHandler, ZooKeeperSignalHandler


def get_signal_handler(zookeeper_client: Client) -> SignalHandler:
  return ZooKeeperSignalHandler(zookeeper_client=zookeeper_client)
