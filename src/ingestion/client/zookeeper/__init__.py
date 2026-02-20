''' Init module for Zookeeper clients. '''

import logging
import os

from .client import KazooClient, KazooZookeeperClient


def get_zookeeper_client() -> KazooZookeeperClient:
  kazoo_client = KazooClient(hosts=os.getenv('ZOO_SERVERS'),
                             logger=logging.getLogger(__name__))
  zookeeper_client = KazooZookeeperClient(kazoo_client=kazoo_client)

  zookeeper_client.start()

  return zookeeper_client
