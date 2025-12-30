"""
Test suite for election facade.
"""

import threading
import unittest
from unittest.mock import ANY, MagicMock

from src.ingestion.election.facade import SequentialEphemeralElectionFacade
from src.ingestion.util.signal_handler import SignalHandler


class SequentialEphemeralSelectionFacadeTestSuite(unittest.TestCase):
  """Test suite for SequentialEphemeralElectionFacade."""

  def setUp(self):
    self._zookeeper_client = MagicMock()

    self._signal_handler = MagicMock(spec=SignalHandler)

    self._zookeeper_client.create.return_value = "/election/znode_000002"
    self._election_facade = SequentialEphemeralElectionFacade(
        zookeeper_client=self._zookeeper_client,
        signal_handler=self._signal_handler)

  def test_should_create_ephemeral_sequential_znode_on_connect(self) -> None:
    self._election_facade.connect()

    self._zookeeper_client.create.assert_called_with("/election/znode_",
                                                     sequential=True,
                                                     ephemeral=True)

  def test_should_become_leader_when_no_other_znodes_present(self) -> None:
    on_leadership_acquired = MagicMock()

    self._zookeeper_client.get_children.return_value = ["znode_000002"]

    self._election_facade.connect()
    self._election_facade.check_leadership_status(
        on_leadership_acquired=on_leadership_acquired)

    on_leadership_acquired.assert_called_once()

  def test_should_become_leader_when_smallest_znode(self) -> None:
    on_leadership_acquired = MagicMock()

    self._zookeeper_client.get_children.return_value = [
        "znode_000002",
        "znode_000003",
        "znode_000004",
    ]

    self._election_facade.connect()
    self._election_facade.check_leadership_status(
        on_leadership_acquired=on_leadership_acquired)

    on_leadership_acquired.assert_called_once()

  def test_should_wait_for_leadership_when_not_smallest_znode(self) -> None:
    on_leadership_acquired = MagicMock()

    self._zookeeper_client.get_children.return_value = [
        "znode_000001",
        "znode_000002",
    ]

    self._election_facade.connect()
    self._election_facade.check_leadership_status(
        on_leadership_acquired=on_leadership_acquired)

    on_leadership_acquired.assert_not_called()
    self._zookeeper_client.get.assert_called_with(path="/election/znode_000001",
                                                  watch=ANY)

  def test_should_stop_leader_election_when_shutdown_event_is_set(self) -> None:
    on_leadership_acquired = MagicMock()

    self._election_facade.connect()
    self._zookeeper_client.get_children.return_value = ["znode_000002"]

    shutdown_event = threading.Event()
    shutdown_event.set()
    self._signal_handler.shutdown_event = shutdown_event

    self._election_facade.run_leader_election_loop(
        on_leadership_acquired=on_leadership_acquired)

    on_leadership_acquired.assert_not_called()

  def test_should_run_leader_election_loop_when_shutdown_event_is_not_set(
      self) -> None:
    on_leadership_acquired = MagicMock()

    self._zookeeper_client.get_children.return_value = ["znode_000002"]

    shutdown_event = threading.Event()
    self._signal_handler.shutdown_event = shutdown_event

    self._election_facade.connect()
    self._election_facade.run_leader_election_loop(
        on_leadership_acquired=on_leadership_acquired)

    on_leadership_acquired.assert_called()
