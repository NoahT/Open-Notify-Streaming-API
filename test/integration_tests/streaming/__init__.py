''' Init module for common dependencies in integration tests. '''

import time
from test.integration_tests.streaming.config import config

from iss_location_client.client import ISSLocationFirestoreClient
from iss_location_client.iss_location import ISSLocation

from src.ingestion.client.publisher.client import RedisPublisherClient

iss_client = ISSLocationFirestoreClient(config=config)

iss_location1 = ISSLocation.from_dict({
    'ts': int(time.time() - 5),
    'pos_la': 1.23,
    'pos_lo': 4.56
})
iss_client.add_iss_location(iss_location=iss_location1)

iss_location2 = ISSLocation.from_dict({
    'ts': (int(time.time()) - 10),
    'pos_la': 7.89,
    'pos_lo': 0.12
})
iss_client.add_iss_location(iss_location2)

publisher_client = RedisPublisherClient(config=config)
