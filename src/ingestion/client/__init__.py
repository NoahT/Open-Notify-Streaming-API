''' Init module for all clients. '''

from cfg_environ.config import Config
from iss_location_client.client import (ISSLocationClient,
                                        ISSLocationFirestoreClient)


def get_iss_firestore_client(config: Config) -> ISSLocationClient:
  iss_firestore_client = ISSLocationFirestoreClient(config=config)

  return iss_firestore_client
