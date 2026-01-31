''' Init for subscriber package '''

from cfg_environ.config import Config

from .client import RedisSubscriberClient, SubscriberClient


def get_subscriber(handler, config: Config) -> SubscriberClient:
  redis_subscriber = RedisSubscriberClient(config=config)
  redis_subscriber.subscribe_iss_location(handler=handler)

  return redis_subscriber
