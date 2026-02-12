''' Init module for event publishing clients. '''
from cfg_environ.config import Config

from .client import PublisherClient, RedisPublisherClient


def get_publisher_client(config: Config) -> PublisherClient:
  client = RedisPublisherClient(config=config)

  return client
