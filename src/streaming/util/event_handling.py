''' Module for event handlers from Redis subscriber. '''

import logging

from flask_sse import sse

_LOGGER_ = logging.Logger(__name__)
_TYPE_ = 'iss_location'


def on_iss_location_update(message: dict) -> None:
  channel = message['channel']
  data = message['data']
  sse.publish(data, type=_TYPE_)
  _LOGGER_.info('Published ISS location update [channel=%s, data=%s]', channel,
                data)
