"""Unit tests for ISS location client."""

import unittest
from unittest.mock import MagicMock, patch

from src.ingestion.client.iss_location.client import ISSLocationFirestoreClient
from src.ingestion.client.iss_location.iss_location import ISSLocation
from src.ingestion.config.config_facade import Config


class ISSLocationFirestoreClientTestSuite(unittest.TestCase):
  '''
  Unit test suite for ISSLocationFirestoreClient
  '''

  def setUp(self):
    config_mock = MagicMock(spec=Config)
    config_mock.read_dict.return_value = {
        'DATABASE_ID': 'open-notify-development',
        'CREATE': {
            'TIMEOUT': 1.000
        },
        'READ': {
            'TIMEOUT': 1.000
        }
    }
    self._config = config_mock
    self._client = ISSLocationFirestoreClient(config=self._config)

  @patch(
      'src.ingestion.client.iss_location.client.credentials.ApplicationDefault')
  @patch(
      'src.ingestion.client.iss_location.client.firebase_admin.initialize_app')
  @patch('src.ingestion.client.iss_location.client.firestore.client')
  def test_should_initialize_firestore_client(self, app_default, init_app,
                                              client) -> None:
    # pylint: disable=pointless-statement
    self._client.firestore_client

    app_default.assert_called_once()
    init_app.assert_called_once()
    client.assert_called_once()

  def test_should_add_iss_location_data(self) -> None:
    collection_mock = MagicMock()
    collection_mock.add.return_value = (12345, MagicMock())

    mock_firestore_client = MagicMock()
    mock_firestore_client.collection.return_value = collection_mock
    with patch.object(self._client,
                      '_firestore_client',
                      new=mock_firestore_client):
      iss_location = ISSLocation(ts=1234567890, pos_la=12.3, pos_lo=-45.6)
      self._client.add_iss_location(iss_location)

      mock_firestore_client.collection.assert_called_once_with('iss_locations')
      collection_mock.add.assert_called_once_with(
          {
              'ts': 1234567890,
              'pos_la': 12.3,
              'pos_lo': -45.6
          }, timeout=1000)

  def test_should_get_iss_location_data(self) -> None:
    iss_location_obj_1 = ISSLocation(ts=1234567890,
                                     pos_la=1.2345,
                                     pos_lo=6.7890)
    iss_location_doc_1 = MagicMock()
    iss_location_doc_1.to_dict.return_value = {
        'ts': 1234567890,
        'pos_la': 1.2345,
        'pos_lo': 6.7890
    }
    iss_location_obj_2 = ISSLocation(ts=1234567895,
                                     pos_la=2.3456,
                                     pos_lo=7.8901)
    iss_location_doc_2 = MagicMock()
    iss_location_doc_2.to_dict.return_value = {
        'ts': 1234567895,
        'pos_la': 2.3456,
        'pos_lo': 7.8901
    }

    query = MagicMock()
    query.where.return_value = query
    query.order_by.return_value = query
    query.get.return_value = [iss_location_doc_1, iss_location_doc_2]

    collection_mock = MagicMock()
    collection_mock.where.return_value = query

    firestore_client = MagicMock()
    firestore_client.collection.return_value = collection_mock
    with patch.object(self._client, '_firestore_client', new=firestore_client):
      results = self._client.get_iss_locations(1234567890, 1234567900)
      self.assertListEqual(results, [iss_location_obj_1, iss_location_obj_2])
