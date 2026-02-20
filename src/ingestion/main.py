'''
Main module for the ingestion service using ZooKeeper for leader election.
'''

import logging
import threading

from iss_location_client.iss_location import ISSLocation

from .client import get_iss_firestore_client
from .client.open_notify import get_open_notify_client
from .client.publisher import get_publisher_client
from .client.zookeeper import get_zookeeper_client
from .config import get_config
from .election import get_facade
from .util import get_signal_handler


def configure_loggging() -> None:
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s %(levelname)s %(name)s: %(message)s')


def on_leadership_acquired(event: threading.Event) -> None:
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
    publisher_client.publish_iss_location(iss_location=iss_location_obj)


configure_loggging()
config = get_config()
open_notify_client = get_open_notify_client(config=config)
iss_firestore_client = get_iss_firestore_client(config=config)
publisher_client = get_publisher_client(config=config)
zookeeper_client = get_zookeeper_client()
zookeeper_client.start()
signal_handler = get_signal_handler(zookeeper_client=zookeeper_client)
election_facade = get_facade(zookeeper_client=zookeeper_client,
                             signal_handler=signal_handler)


def main() -> None:
  try:
    zookeeper_client.start()
    election_facade.run_leader_election_loop(
        on_leadership_acquired=on_leadership_acquired)
  finally:
    zookeeper_client.stop()


if __name__ == '__main__':
  main()
