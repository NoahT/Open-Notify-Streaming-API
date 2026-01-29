''' Module for testing event handlers for subscribed events '''

import json
from unittest import TestCase
from unittest.mock import patch

from iss_location_client.iss_location import ISSLocation

from src.streaming.util.event_handling import on_iss_location_update


class EventHandlingTestSuite(TestCase):
  ''' Unit test suite for subscribed event handling. '''

  @patch('src.streaming.util.event_handling.sse')
  def test_should_call_flask_sse_for_iss_location_update(
      self, flask_sse_mock) -> None:
    message_data = ISSLocation.from_dict({
        'ts': 123,
        'pos_la': 4.56,
        'pos_lo': 7.89
    })
    message_data_json = json.dumps(message_data.iss_dict)
    on_iss_location_update({
        'channel': 'iss_location',
        'data': message_data_json
    })

    flask_sse_mock.publish.assert_called_once()
