"""
ZooKeeper client wrapper using Kazoo library.
"""

from abc import ABC, abstractmethod
from types import FunctionType

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
