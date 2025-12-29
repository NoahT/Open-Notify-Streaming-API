"""
Test suite for Open Notify client.
"""

import unittest
from unittest.mock import MagicMock, Mock

import requests
from requests import HTTPError

from src.ingestion.client.open_notify.client import OpenNotifyRequestsClient


class OpenNotifyRequestsClientTestSuite(unittest.TestCase):
  """Test suite for OpenNotifyRequestsClient."""

  def setUp(self):
    self._client = OpenNotifyRequestsClient()

  def test_should_get_iss_data_for_2xx_response(self) -> None:
    mock_response_json = {
        "iss_position": {
            "latitude": "38.2750",
            "longitude": "132.3841"
        },
        "message": "success",
        "timestamp": 1767045061
    }
    mock_response = MagicMock(spec=requests.Response)
    mock_response.json.return_value = mock_response_json
    requests.get = MagicMock()
    requests.get.return_value = mock_response

    response = self._client.get_iss()

    self.assertEqual(response, mock_response_json)

  def test_should_raise_error_for_5xx_response(self) -> None:
    mock_response = MagicMock(spec=requests.Response)
    mock_response.raise_for_status = Mock(side_effect=HTTPError())
    requests.get = MagicMock()
    requests.get.return_value = mock_response

    self.assertRaises(requests.HTTPError, self._client.get_iss)
