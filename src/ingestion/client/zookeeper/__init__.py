from kazoo.client import KazooClient
from .client import KazooZookeeperClient
import logging
import os

client = KazooZookeeperClient(KazooClient(hosts=os.getenv('ZOO_SERVERS'), logger=logging.getLogger(__name__)))
