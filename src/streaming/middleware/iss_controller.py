''' Controller module for ISS resources. '''

import logging
from abc import ABC, abstractmethod

from cfg_environ.config import Config
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES

from .iss_repository import ISSRepository


class ISSController(ABC):
  '''
  Abstract base class for routing ISS resources.
  '''

  @abstractmethod
  def v1_iss_events(self) -> list:
    '''
    Controller routing for GET::/v1/iss/events
    
    :param self: Current ISSController instance.
    :return: List of serialized ISSPosition instances.
    :rtype: list
    '''
    pass


class V1ISSController(ISSController):
  '''
  ISSController implementation for v1 based routing logic.
  '''

  def __init__(self,
               repository: ISSRepository,
               config: Config,
               logger: logging.Logger = logging.Logger(__name__)):
    self._repository = repository
    self._config = config
    self._logger = logger

  def v1_iss_events(self, window: int = 30) -> list:
    self._validate_v1_iss_events(window=window)
    iss_events = self._repository.get_iss_locations(window=window)

    return iss_events

  def _validate_v1_iss_events(self, window: int) -> None:
    config_v1_iss_events = self._config.read_dict('ROUTES')['V1_ISS_EVENTS']
    config_window = config_v1_iss_events['PARAMS']['WINDOW']
    window_min = config_window['MINIMUM_VALUE']
    window_max = config_window['MAXIMUM_VALUE']

    if window not in range(window_min, window_max):
      raise HTTPException(HTTP_STATUS_CODES[400],
                          f'Invalid window size: {window}')
