"""
ZooKeeper client wrapper using Kazoo library.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from types import FunctionType

from hyx.retry import retry
from kazoo.client import KazooClient
from kazoo.protocol.states import ZnodeStat


class Client(ABC):
  """
    Abstract base class for Zookeeper client, which we use to interface
    with the Zookeeper instances in our ensemble.
    """

  @abstractmethod
  def start(self) -> None:
    pass

  @abstractmethod
  def stop(self) -> None:
    pass

  @abstractmethod
  def add_listener(self, listener: FunctionType) -> None:
    pass

  @abstractmethod
  def create(self, path: str, value: bytes, sequential: bool,
             ephemeral: bool) -> None:
    pass

  @abstractmethod
  def set(self, path: str, value: bytes) -> None:
    pass

  @abstractmethod
  def get(self, path: str, watch: FunctionType) -> ZnodeStat:
    pass

  @abstractmethod
  def get_children(self, path: str) -> list:
    pass


class KazooZookeeperClient(Client):
  """
    Kazoo client implementation for interfacing with hosts in a Zookeeper
    ensemble. We created this wrapper around the kazoo client itself to make
    testing easier, in case we need to instrument interactions with Zookeeper
    with logging and monitoring, etc.
    """

  def __init__(self, kazoo_client: KazooClient):
    super().__init__()
    self._kazoo_client = kazoo_client

  def start(self) -> None:
    self._kazoo_client.start()

  def stop(self) -> None:
    self._kazoo_client.stop()

  def add_listener(self, listener: FunctionType) -> None:
    self._kazoo_client.add_listener(listener)

  def create(self,
             path: str,
             value: bytes = b'',
             sequential: bool = False,
             ephemeral: bool = False) -> str:
    if self._kazoo_client.exists(path):
      self._kazoo_client.logger.warning('Path already exists: ' + path)
      return None
    else:
      return self._kazoo_client.create(path,
                                       value,
                                       makepath=True,
                                       sequence=sequential,
                                       ephemeral=ephemeral)

  def set(self, path: str, value: bytes = b'') -> None:
    self._kazoo_client.set(path, value)

  def get(self, path: str, watch: FunctionType = None) -> ZnodeStat:
    return self._kazoo_client.get(path, watch=watch)

  def get_children(self, path: str) -> list:
    return self._kazoo_client.get_children(path)


class FaultTolerantKazooZookeeperClient(Client):
  '''
  ZookeeperClient wrapper using fault tolerance primtives for
  resiliency.
  '''

  def __init__(self,
               client: Client,
               logger: logging.Logger = logging.getLogger(__name__)):
    self._client = client
    self._logger = logger

  def start(self) -> None:
    return asyncio.run(self._start())

  @retry(on=Exception, attempts=3, backoff=1)
  async def _start(self) -> None:
    return await self._client.start()

  def stop(self) -> None:
    return asyncio.run(self._stop())

  @retry(on=Exception, attempts=3, backoff=1)
  async def _stop(self) -> None:
    return await self._client.stop()

  def add_listener(self, listener: FunctionType) -> None:
    return asyncio.run(self._add_listener(listener=listener))

  @retry(on=Exception, attempts=3, backoff=1)
  async def _add_listener(self, listener: FunctionType) -> None:
    return await self._client.add_listener(listener=listener)

  def create(self, path: str, value: bytes, sequential: bool,
             ephemeral: bool) -> None:
    return asyncio.run(
        self._create(path=path,
                     value=value,
                     sequential=sequential,
                     ephemeral=ephemeral))

  @retry(on=Exception, attempts=3, backoff=1)
  async def _create(self, path: str, value: bytes, sequential: bool,
                    ephemeral: bool) -> None:
    return await self._client.create(path=path,
                                     value=value,
                                     sequential=sequential,
                                     ephemeral=ephemeral)

  def set(self, path: str, value: bytes) -> None:
    return asyncio.run(self._set(path=path, value=value))

  @retry(on=Exception, attempts=3, backoff=1)
  async def _set(self, path: str, value: bytes) -> None:
    return await self._client.set(path=path, value=value)

  def get(self, path: str, watch: FunctionType) -> ZnodeStat:
    return asyncio.run(self._get(path=path, watch=watch))

  @retry(on=Exception, attempts=3, backoff=1)
  async def _get(self, path: str, watch: FunctionType) -> ZnodeStat:
    return await self._client.get(path=path, watch=watch)

  def get_children(self, path: str) -> list:
    return asyncio.run(self._get_children(path=path))

  @retry(on=Exception, attempts=3, backoff=1)
  async def _get_children(self, path: str) -> list:
    return await self._client.get_children(path=path)
