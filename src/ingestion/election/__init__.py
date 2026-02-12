''' Init module for leader election. '''

import logging

from ..client.zookeeper.client import KazooZookeeperClient
from ..util.signal_handler import SignalHandler
from .facade import ElectionFacade, SequentialEphemeralElectionFacade


def get_facade(zookeeper_client: KazooZookeeperClient,
               signal_handler: SignalHandler) -> ElectionFacade:
  election_facade = SequentialEphemeralElectionFacade(
      zookeeper_client=zookeeper_client,
      signal_handler=signal_handler,
      logger=logging.getLogger(__name__))
  election_facade.connect()

  return election_facade
