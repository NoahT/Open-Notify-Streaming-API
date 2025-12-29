import logging
from abc import ABC, abstractmethod
from logging import Logger

import requests
from requests import HTTPError


class OpenNotifyClient(ABC):
  """
  Abstract base class for Open Notify API client 
  http://open-notify.org/Open-Notify-API/ISS-Location-Now/
  """

  @abstractmethod
  def get_iss(self):
    pass


class OpenNotifyRequestsClient(OpenNotifyClient):
  """
  Open Notify API client implementation with requests module.
  """

  def __init__(self,
               hostname: str = 'https://api.open-notify.org',
               timeout: float = 2,
               logger: Logger = logging.getLogger(__name__)):
    self._hostname = hostname
    self._iss_path = '/iss-now.json'
    self._timeout = timeout
    self._logger = logger

  def get_iss(self):
    endpoint = f'{self._hostname}{self._iss_path}'
    self._logger.warning(f'Requesting for ISS data [endpoint={endpoint}]')
    response = requests.get(endpoint, timeout=self._timeout)
    response.raise_for_status()
    response_json = response.json()

    self._logger.warning(
        'Successfully requested for ISS data [response_json=%s]', response_json)

    return response_json
