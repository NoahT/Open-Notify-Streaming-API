''' Module for ISS location subscriber implementations. '''
import logging
from abc import ABC, abstractmethod

import redis

from ...config.config_facade import Config


class SubscriberClient(ABC):
  '''
  Abstract base class for subscribing to ISS location updates.
  '''

  @abstractmethod
  def subscribe_iss_location(self, handler) -> None:
    '''
    Abstract method used to add an async handler for ISS location 
    updates.
    
    :param self: Current SubscriberClient instance.
    :param handler: The async handler to use for ISS location updates.
    :type handler: function
    '''
    pass


class RedisSubscriberClient(SubscriberClient):
  '''
  SusbscriberClient implementation which uses Redis channels to subscribe to 
  ISS location updates.
  '''

  def __init__(
      self,
      config: Config,
      logger: logging.Logger = logging.getLogger(__name__)) -> None:
    self._config = config.read_dict('REDIS_CLIENT')
    self._logger = logger
    self._client = None
    self._subscriber_thread = None

  def subscribe_iss_location(self, handler) -> None:
    pubsub = self.client.pubsub()
    channel = self._config['CHANNEL']
    sleep_time = self._config['SUBSCRIBE']['SLEEP_TIME']
    pubsub.subscribe(**{channel: handler})
    self._subscriber_thread = pubsub.run_in_thread(sleep_time=sleep_time)

    self._logger.info(
        f'Subscribed to channel [channel={channel}, sleep_time={sleep_time}]')

  @property
  def client(self) -> redis.Redis:
    if not self._client:
      host = self._config['HOST']
      socket_connect_timeout = self._config['CONNECT']['TIMEOUT']
      decode_responses = self._config['DECODE_RESPONSES']
      self._client = redis.Redis(host=host,
                                 socket_connect_timeout=socket_connect_timeout,
                                 decode_responses=decode_responses)

      self._logger.info(f'Initialized redis subscriber [host={host}]')

    return self._client
