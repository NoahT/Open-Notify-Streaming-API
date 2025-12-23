from kazoo.client import KazooClient
from kazoo.protocol.states import ZnodeStat
from abc import ABC, abstractmethod

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
    def add_listener(self, listener) -> None:
        pass

    @abstractmethod
    def create(self, path, value) -> None:
        pass
    
    @abstractmethod
    def set(self, path, value) -> None:
        pass

    @abstractmethod
    def get(self, path) -> ZnodeStat:
        pass

class KazooZookeeperClient(Client):
    """
    Kazoo client implementation for interfacing with a local Zookeeper instance.
    """

    def __init__(self, kazoo_client: KazooClient):
        super().__init__()
        self._kazoo_client = kazoo_client

    def start(self) -> None:
        self._kazoo_client.start()
    
    def stop(self) -> None:
        self._kazoo_client.stop()
    
    def add_listener(self, listener) -> None:
        self._kazoo_client.add_listener(listener)
    
    def create(self, path, value) -> None:
        if self._kazoo_client.exists(path):
            self._kazoo_client.logger.warning('Path already exists: ' + path)
        else:
            self._kazoo_client.create(path, value, makepath=True)
    
    def set(self, path, value) -> None:
        self._kazoo_client.set(path, value)
    
    def get(self, path) -> ZnodeStat:
        return self._kazoo_client.get(path)
