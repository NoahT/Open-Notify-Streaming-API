"""
Test suite for election facade.
"""

import unittest
from unittest.mock import ANY, MagicMock

from src.ingestion.election.facade import SequentialEphemeralElectionFacade


class SequentialEphemeralSelectionFacadeTestSuite(unittest.TestCase):
  """Test suite for SequentialEphemeralElectionFacade."""

  def setUp(self):
    self._zookeeper_client = MagicMock()
    self._zookeeper_client.create.return_value = "/election/znode_000002"
    self._election_facade = SequentialEphemeralElectionFacade(
        zookeeper_client=self._zookeeper_client)

  def test_should_create_ephemeral_sequential_znode_on_connect(self) -> None:
    self._election_facade.connect()

    self._zookeeper_client.create.assert_called_with("/election/znode_",
                                                     sequential=True,
                                                     ephemeral=True)

  def test_should_become_leader_when_no_other_znodes_present(self) -> None:
    leader_func = MagicMock()

    self._election_facade.connect()
    self._zookeeper_client.get_children.return_value = ["znode_000002"]
    self._election_facade.check_leadership_status(leader_func=leader_func)

    leader_func.assert_called_once()

  def test_should_become_leader_when_smallest_znode(self) -> None:
    leader_func = MagicMock()

    self._election_facade.connect()
    self._zookeeper_client.get_children.return_value = [
        "znode_000002",
        "znode_000003",
        "znode_000004",
    ]
    self._election_facade.check_leadership_status(leader_func=leader_func)

    leader_func.assert_called_once()

  def test_should_wait_for_leadership_when_not_smallest_znode(self) -> None:
    leader_func = MagicMock()

    self._election_facade.connect()
    self._zookeeper_client.get_children.return_value = [
        "znode_000001",
        "znode_000002",
    ]
    self._election_facade.check_leadership_status(leader_func=leader_func)

    leader_func.assert_not_called()
    self._zookeeper_client.get.assert_called_with(path="/election/znode_000001",
                                                  watch=ANY)
