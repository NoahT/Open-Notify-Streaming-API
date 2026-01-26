''' Client for publishing ISS location updates. '''
import json
import logging
from abc import ABC, abstractmethod

import redis
from cfg_environ.config import Config
from iss_location_client.iss_location import ISSLocation


class PublisherClient(ABC):
  '''
  Abstract base class for publishing ISS location updates to a
  messaging broker.
  '''

  @abstractmethod
  def publish_iss_location(self, iss_location: ISSLocation) -> bool:
    '''
    Publish an ISS location update.
    
    :param self: Current PublisherClient instance.
    :param iss_location: The ISS location update to publish.
    :type iss_location: ISSLocation
    :return: Whether the message successfully published.
    :rtype: bool
    '''
    pass


class RedisPublisherClient(PublisherClient):
  '''
  Redis based publisher client for ISS location updates.
  '''

  def __init__(self,
               config: Config,
               logger: logging.Logger = logging.getLogger(__name__)):
    self._client = None
    self._config = config.read_dict('REDIS_CLIENT')
    self._logger = logger

  def publish_iss_location(self, iss_location: ISSLocation) -> bool:
    is_published = False
    channel = self._config['CHANNEL']
    message = json.dumps(iss_location.iss_dict)
    try:
      subscribers = self.client.publish(channel=channel, message=message)

      self._logger.info(
          ('Published ISS location update ', f'[channel={channel}, ',
           f'message={message}, ', f'subscribers={subscribers}]'))
      is_published = True
    #pylint: disable=broad-exception-caught
    except Exception as exception:
      self._logger.error(
          ('Failed publishing ISS location update ', f'[channel={channel}, ',
           f'message={message}, ', f'error={exception}]'))

    return is_published

  @property
  def client(self) -> redis.Redis:
    if not self._client:
      host = self._config['HOST']
      port = self._config['PORT']
      connect_timeout = self._config['CONNECT']['TIMEOUT']
      publish_timeout = self._config['PUBLISH']['TIMEOUT']

      self._logger.info(f'Initialized Redis client [host={host}, port={port}]')

      self._client = redis.Redis(host=host,
                                 port=port,
                                 socket_connect_timeout=connect_timeout,
                                 socket_timeout=publish_timeout)

    return self._client
