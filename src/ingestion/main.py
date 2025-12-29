"""
Main module for the ingestion service using ZooKeeper for leader election.
"""

import logging
import os

from kazoo.client import KazooClient

from .client.zookeeper.client import KazooZookeeperClient
from .election.facade import SequentialEphemeralElectionFacade


def leadership_func():
  logging.warning("Obtained leadership")


client = KazooZookeeperClient(kazoo_client=KazooClient(
    hosts=os.getenv("ZOO_SERVERS"), logger=logging.getLogger(__name__)))
client.start()
election_facade = SequentialEphemeralElectionFacade(
    zookeeper_client=client, logger=logging.getLogger(__name__))
election_facade.connect()

if __name__ == "__main__":
  while True:
    event = election_facade.check_leadership_status(leader_func=leadership_func)

    if not event:
      break

    event.wait()
