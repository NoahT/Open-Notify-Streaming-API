from kazoo.client import KazooClient
from .client import KazooZookeeperClient
import logging


client = KazooZookeeperClient(KazooClient(hosts='127.0.0.1:2181', logger=logging.getLogger(__name__)))
