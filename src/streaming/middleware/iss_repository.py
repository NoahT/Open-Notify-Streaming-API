''' Module defining how and where ISS data is collected and stored. '''
import logging
import time
from abc import ABC, abstractmethod

from iss_location_client.client import ISSLocationClient


class ISSRepository(ABC):
  '''
  Class used to abstract how and where we query for ISS data.
  '''

  @abstractmethod
  def get_iss_locations(self, window: int) -> list:
    '''
    Get ISS location data on the rolling window [now - window, now]
    
    :param self: Current ISSRepository instance.
    :param window: The size of the rolling window in seconds.
    :type window: int
    :return: List of ISSLocation instances.
    :rtype: ISSLocation
    '''
    pass


class ISSPassThroughRepository(ISSRepository):
  '''
  ISSRepository implementation that provides results based on the 
  the chosen ISSLocation client.
  '''

  def __init__(self,
               client: ISSLocationClient,
               logger: logging.Logger = logging.getLogger(__name__)):
    self._client = client
    self._logger = logger

  def get_iss_locations(self, window: int) -> list:
    ts_to = int(time.time())
    ts_from = ts_to - window
    self._logger.info('Getting ISS locations [ts_from=%s, ts_to=%s]', ts_from,
                      ts_to)
    iss_locations = self._client.get_iss_locations(ts_from=ts_from, ts_to=ts_to)
    self._logger.info(
        'Received ISS locations [ts_from=%s, ts_to=%s, length=%s]', ts_from,
        ts_to, len(iss_locations))

    return iss_locations
