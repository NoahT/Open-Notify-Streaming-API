import logging
import signal
import threading
from abc import ABC, abstractmethod

from ..client.zookeeper.client import Client


class SignalHandler(ABC):
  """
    Abstract base class for gracefully handling termination of the ingestion
    service.
    """

  @abstractmethod
  def handle_shutdown(self, signum, frame) -> None:
    """
    Abstract method used to handle shutdown on signal termination or
    signal iterrupt.
    
    :param self: Current SignalHandler instance.
    :param signum: The signal number
    :param frame: The stack frame.
    """
    pass


class ZooKeeperSignalHandler(SignalHandler):
  """
  Implementation of SignalHandler used to gracefully terminate 
  the running ZooKeeper instance.
  """

  def __init__(self,
               zookeeper_client: Client,
               logger: logging.Logger = logging.getLogger(__name__)):
    self._shutdown_event = threading.Event()
    self._zookeeper_client = zookeeper_client
    self._logger = logger

    self._add_signal_handlers()

  def handle_shutdown(self, signum, frame) -> None:
    self._logger.warning('Handling shutdown for ZooKeeper instance [signum=%s]',
                         signum)
    self._zookeeper_client.stop()
    self._shutdown_event.set()

  def _add_signal_handlers(self) -> None:
    signal.signal(signal.SIGTERM, self.handle_shutdown)
    signal.signal(signal.SIGINT, self.handle_shutdown)

  @property
  def shutdown_event(self) -> threading.Event:
    return self._shutdown_event
