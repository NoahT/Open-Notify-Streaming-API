''' Init for subscriber package '''

from cfg_environ.config import Config

from .client import RedisSubscriberClient, SubscriberClient


def get_subscriber(config: Config) -> SubscriberClient:
  redis_subscriber = RedisSubscriberClient(config=config)

  return redis_subscriber
