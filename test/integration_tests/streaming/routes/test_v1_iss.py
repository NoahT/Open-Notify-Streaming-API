''' Module to test V1 APIs for streaming service. '''

import threading
import time
from test.integration_tests.streaming import (iss_location1, iss_location2,
                                              publisher_client)
from test.integration_tests.streaming.config import config
from unittest import TestCase

import requests
from iss_location_client.iss_location import ISSLocation


class V1ISSTestSuite(TestCase):
  ''' Integration test suite for V1 APIs. '''

  def setUp(self):
    self._config = config

  def test_should_return_iss_locations_within_input_window(self) -> None:
    params = {'window': 300}
    response = requests.get(url=self.v1_iss_location,
                            params=params,
                            timeout=self.timeout)

    response_json = response.json()
    self.assertIsNotNone(response_json)

    iss_locations = response_json['locations']
    self.assertEqual(2, len(iss_locations))
    self.assertTrue(
        any(
            ISSLocation.from_dict(iss_location) == iss_location1
            for iss_location in iss_locations))
    self.assertTrue(
        any(
            ISSLocation.from_dict(iss_location) == iss_location2
            for iss_location in iss_locations))

  def test_should_return_400_when_input_window_below_min(self) -> None:
    params = {'window': 9}
    response = requests.get(url=self.v1_iss_location,
                            params=params,
                            timeout=self.timeout)

    self.assertEqual(400, response.status_code)

  def test_should_return_400_when_input_window_above_max(self) -> None:
    params = {'window': 601}
    response = requests.get(url=self.v1_iss_location,
                            params=params,
                            timeout=self.timeout)

    self.assertEqual(400, response.status_code)

  def test_should_send_server_sent_events_on_iss_location_update(self) -> None:

    def stream(threshold: int):
      events_processed = 0
      # Timeouts are not relevant for server sent events since we keep the
      # HTTP connection open.
      # pylint:disable=missing-timeout
      response = requests.get(url=self.v1_iss_stream, stream=True)

      for line in response.iter_lines():
        if line:
          decoded_line = line.decode('utf-8')
          if 'data' in decoded_line:
            events_processed += 1

        if events_processed >= threshold:
          has_streamed_event.set()
          response.close()

    is_event_successful = False
    has_streamed_event = threading.Event()
    stream_response = threading.Thread(target=stream, args=(2,), daemon=True)
    try:
      stream_response.start()

      for _ in range(3):
        iss_location = ISSLocation.from_dict({
            'ts': int(time.time()),
            'pos_la': 1.234,
            'pos_lo': 5.678
        })
        publisher_client.publish_iss_location(iss_location=iss_location)
        time.sleep(1)

      is_event_successful = has_streamed_event.is_set()
    finally:
      has_streamed_event.set()

    self.assertTrue(is_event_successful)

  @property
  def timeout(self) -> float:
    return self._config.read_dict('STREAMING_CLIENT')['READ']['TIMEOUT']

  @property
  def v1_iss_location(self) -> str:
    resource_path = '/v1/iss/location'

    return f'{self.host}{resource_path}'

  @property
  def v1_iss_stream(self) -> str:
    resource_path = '/v1/iss/stream'

    return f'{self.host}{resource_path}'

  @property
  def host(self) -> str:
    config_streaming_client = self._config.read_dict('STREAMING_CLIENT')
    host = config_streaming_client['HOST']
    port = config_streaming_client['PORT']

    return f'http://{host}:{port}'
