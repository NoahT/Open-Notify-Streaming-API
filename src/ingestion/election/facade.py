from abc import ABC, abstractmethod
from ..client.zookeeper.client import KazooZookeeperClient
from kazoo.protocol.states import EventType, WatchedEvent
from logging import Logger
from types import FunctionType
import threading

class ElectionFacade(ABC):
    """
    Abstract base class used to provide a simplified interface for
    leader election among all ZooKeeper instances.
    """

    @abstractmethod
    def connect(self) -> None:
        """
        Abstract method used for initialization when a ZooKeeper server
        first connects into the ensemble.
        
        :param self: Current instance of ElectionFacade.
        """
        pass

    def check_leadership_status(self, leader_func: FunctionType) -> threading.Event:
        """
        Abstract method used to check for leadership status for the current
        ZooKeeper server instance.
        
        :param self: Current instance of ElectionFacade.
        :param leader_func: Function reference invoked when the current ZooKeeper server is the leader.
        :type leader_func: function
        :return: Event in the instance where the current instance cannot obtain leadership.
        :rtype: threading.Event
        """
        pass

class SequentialEphemeralElectionFacade(ElectionFacade):
    """
    Leader election implementation with sequential ephemeral znodes.
    """
    def __init__(self, zookeeper_client: KazooZookeeperClient, znode_root_path: str='/election', logger: Logger=Logger(__name__)):
        self._logger = logger
        self._znode_root_path = znode_root_path
        self._zookeeper_client = zookeeper_client

        self._logger.warning(f'Initialized election facade [znode_root_path={znode_root_path}]')
        self._initialize_znode_election_path()

    def connect(self) -> None:
        znode = self._zookeeper_client.create(f'{self._znode_root_path}/znode_', sequential=True, ephemeral=True)
        self._znode = znode
        self._logger.warning(f'Connected znode for zookeeper instance [znode_path={znode}]')

    def check_leadership_status(self, leader_func: FunctionType) -> threading.Event:
        # Using child znode names and non-prefixed znode name, we can determine if there
        # is a node that precedes the current.
        sorted_children = self._get_sorted_children()
        self._logger.warning(f'Retrieved znodes for election [sorted_children={sorted_children}]')
        znode_name = self._znode.removeprefix(f'{self._znode_root_path}/')
        znode_index = sorted_children.index(znode_name)

        self._logger.warning(f'Retrieved index of current znode [znode_name={znode_name}, znode_index={znode_index}]')

        if znode_index == 0:
            self._logger.warning(f'Electing znode as leader [znode={self._znode}]')
            # If the index is 0, the newly created znode has the lowest id and is leader by default
            leader_func()
            return None
        else:
            # If the index is not 0, we need to watch the preceding znode to re-check for leadership status.
            watch_index = znode_index - 1
            znode_watch = sorted_children[watch_index]
            # get_children() only gets the child znode names, so we need to watch based on the absolute path for
            # the preceding znode.
            znode_watch_path = f'{self._znode_root_path}/{znode_watch}'

            watch_event = self._get_watch_event()
            def watch_callback(event: WatchedEvent):
                self._logger.warning(f'Watch event on znode [path={event.path}, type={event.type}]')
                if event.type == EventType.DELETED:
                    watch_event.set()
            
            self._zookeeper_client.get(path=znode_watch_path, watch=watch_callback)
            self._logger.warning(f'Added watch to next lowest znode [znode_watch_path={znode_watch_path}]')
            return watch_event

    def _get_watch_event(self) -> threading.Event:
        return threading.Event()
    
    def _initialize_znode_election_path(self) -> None:
        path = self._zookeeper_client.create(self._znode_root_path, None)
        self._logger.warning(f'Initialized election path [path={path}]')
    
    def _get_sorted_children(self) -> list:
        children = self._zookeeper_client.get_children(self._znode_root_path)
        sorted_children = sorted(children)
        # Child znode names sorted without path prefix
        return sorted_children
