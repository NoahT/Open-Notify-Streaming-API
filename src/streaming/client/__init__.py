''' Init for client package. '''

from cfg_environ.config import Config
from iss_location_client.client import (ISSLocationClient,
                                        ISSLocationFirestoreClient)


def get_iss_client(config: Config) -> ISSLocationClient:
  client = ISSLocationFirestoreClient(config=config)

  return client
