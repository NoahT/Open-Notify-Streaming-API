"""
Main module for the ingestion service using ZooKeeper for leader election.
"""

import logging
import os
import threading

from kazoo.client import KazooClient

from .client.iss_location.client import ISSLocationFirestoreClient
from .client.iss_location.iss_location import ISSLocation
from .client.open_notify.client import OpenNotifyRequestsClient
from .client.zookeeper.client import Client, KazooZookeeperClient
from .config.config_facade import Config, ConfigFacade
from .election.facade import ElectionFacade, SequentialEphemeralElectionFacade
from .util.signal_handler import SignalHandler, ZooKeeperSignalHandler


def configure_loggging() -> None:
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s %(levelname)s %(name)s: %(message)s')


def get_config() -> Config:
  config = ConfigFacade('ingestion/config', 'development', 'default')

  return config


def get_open_notify_client() -> OpenNotifyRequestsClient:
  open_notify_client = OpenNotifyRequestsClient()
  return open_notify_client


def get_iss_firestore_client() -> ISSLocationFirestoreClient:
  config = get_config()
  iss_firestore_client = ISSLocationFirestoreClient(config=config)

  return iss_firestore_client


def on_leadership_acquired(event: threading.Event) -> None:
  open_notify_client = get_open_notify_client()
  iss_firestore_client = get_iss_firestore_client()
  logging.warning('Obtained leadership')
  while not event.is_set():
    event.wait(5)
    iss_location = open_notify_client.get_iss()
    logging.warning('Short polling ISS location data [payload=%s]',
                    iss_location)

    iss_location_obj = ISSLocation(
        ts=iss_location['timestamp'],
        pos_la=iss_location['iss_position']['latitude'],
        pos_lo=iss_location['iss_position']['longitude'])

    iss_firestore_client.add_iss_location(iss_location=iss_location_obj)
    logging.warning('Upserted ISS location data [iss_location_obj=%s]',
                    iss_location_obj)


def get_zookeeper_client() -> KazooZookeeperClient:
  kazoo_client = KazooClient(hosts=os.getenv('ZOO_SERVERS'),
                             logger=logging.getLogger(__name__))
  zookeeper_client = KazooZookeeperClient(kazoo_client=kazoo_client)

  return zookeeper_client


def get_facade(zookeeper_client: KazooZookeeperClient,
               signal_handler: SignalHandler) -> ElectionFacade:
  election_facade = SequentialEphemeralElectionFacade(
      zookeeper_client=zookeeper_client,
      signal_handler=signal_handler,
      logger=logging.getLogger(__name__))
  election_facade.connect()

  return election_facade


def get_signal_handler(zookeeper_client: Client) -> SignalHandler:
  return ZooKeeperSignalHandler(zookeeper_client=zookeeper_client)


def main() -> None:
  configure_loggging()
  zookeeper_client = get_zookeeper_client()
  try:
    zookeeper_client.start()
    signal_handler = get_signal_handler(zookeeper_client=zookeeper_client)
    election_facade = get_facade(zookeeper_client=zookeeper_client,
                                 signal_handler=signal_handler)
    election_facade.run_leader_election_loop(
        on_leadership_acquired=on_leadership_acquired)
  finally:
    zookeeper_client.stop()


if __name__ == '__main__':
  main()
