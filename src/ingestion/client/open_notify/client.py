'''
Open Notify client module for ISS location API.
'''

import asyncio
import logging
from abc import ABC, abstractmethod
from logging import Logger

import requests
from hyx.circuitbreaker import consecutive_breaker
from hyx.retry import retry
from requests.exceptions import HTTPError


class OpenNotifyClient(ABC):
  '''
  Abstract base class for Open Notify API client 
  http://open-notify.org/Open-Notify-API/ISS-Location-Now/
  '''

  @abstractmethod
  def get_iss(self) -> dict:
    pass


class OpenNotifyRequestsClient(OpenNotifyClient):
  '''
  Open Notify API client implementation with requests module.
  '''

  def __init__(self,
               hostname: str = 'http://api.open-notify.org',
               timeout: float = 15,
               logger: Logger = logging.getLogger(__name__)):
    self._hostname = hostname
    self._iss_path = '/iss-now.json'
    self._timeout = timeout
    self._logger = logger

  def get_iss(self) -> dict:
    endpoint = f'{self._hostname}{self._iss_path}'
    self._logger.warning(f'Requesting for ISS data [endpoint={endpoint}]')
    response = requests.get(endpoint, timeout=self._timeout)
    response.raise_for_status()
    response_json = response.json()

    self._logger.warning(
        'Successfully requested for ISS data [response_json=%s]', response_json)

    return response_json


class FaultTolerantOpenNotifyRequestsClient(OpenNotifyClient):
  '''
  Open Notify API client with retries and circuit breaker pattern.
  '''

  breaker = consecutive_breaker(exceptions=(requests.Timeout, HTTPError),
                                failure_threshold=5,
                                recovery_time_secs=30,
                                recovery_threshold=1)

  def __init__(self, client: OpenNotifyClient):
    self._client = client

  def get_iss(self) -> dict:
    return asyncio.run(self._get_iss_from_client())

  @retry(on=(requests.Timeout, HTTPError), attempts=3, backoff=1)
  @breaker
  async def _get_iss_from_client(self) -> dict:
    # Circuit breaker with hyx wraps the decorated function with an async
    # wrapper function. This creates a coroutine, so we need to create a
    # separate method for this and call asyncio.run(..) to prevent the
    # interpreter from throwing any warnings.
    return self._client.get_iss()
