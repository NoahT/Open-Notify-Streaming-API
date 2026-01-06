import logging
from abc import ABC, abstractmethod

import firebase_admin
from firebase_admin import credentials, firestore

from ...config.config_facade import Config
from .iss_location import ISSLocation


class ISSLocationClient(ABC):
  '''
  Abstract base class for storing and reading ISS location data.
  '''

  @abstractmethod
  def add_iss_location(self, iss_location: ISSLocation) -> None:
    '''
    Add ISS location data to data store.
    
    :param self: Current ISSLocationClient instance.
    :param iss_location: ISS location data to add.
    :type iss_location: ISSLocation
    '''
    pass

  @abstractmethod
  def get_iss_locations(self, ts_from: int, ts_to: int) -> list:
    '''
    Get ISS location data on the UNIX timestamp window [ts_from, ts_to]
    
    :param self: Current ISSLocationClient instance.
    :param ts_from: UNIX timestamp for lower bound.
    :type ts_from: int
    :param ts_to: UNIX timestamp for upper bound.
    :type ts_to: int
    :return: List of ISSLocation objects.
    :rtype: list
    '''
    pass


class ISSLocationFirestoreClient(ISSLocationClient):
  '''
  Google Cloud Firestore client implementation for storing and reading 
  ISS location data.
  '''

  ISS_COLLECTION_NAME = 'iss_locations'

  def __init__(
      self,
      config: Config,
      logger: logging.Logger = logging.getLogger(__name__)) -> None:
    self._config = config
    self._logger = logger
    self._firestore_client = None

  def add_iss_location(self, iss_location: ISSLocation) -> None:
    timeout = self.firestore_config['CREATE']['TIMEOUT'] * 1000

    self._logger.warning(
        f'Adding iss_location [iss_location={iss_location}, timeout={timeout}]')

    document_tuple = self.firestore_client.collection(
        self.ISS_COLLECTION_NAME).add(iss_location.iss_dict, timeout=timeout)

    self._logger.info(f'Added iss_location [document={document_tuple[1]}]')

  def get_iss_locations(self, ts_from: int, ts_to: int) -> list:
    timeout = self.firestore_config['READ']['TIMEOUT'] * 1000
    self._logger.info(
        f'Retrieving ISS location data [ts_from={ts_from}, ts_to={ts_to}, timeout={timeout}]'
    )

    documents = self.firestore_client.collection(
        self.ISS_COLLECTION_NAME).where('ts', '>=', ts_from).where(
            'ts', '<=', ts_to).order_by('ts').get(timeout=timeout)

    iss_locations = [
        ISSLocation.from_dict(document.to_dict()) for document in documents
    ]

    self._logger.info(
        f'Retrieved ISS location data [iss_locations={iss_locations}]')

    return iss_locations

  @property
  def firestore_config(self) -> dict:
    firestore_config = self._config.read_dict('FIRESTORE_CLIENT_CONFIG')

    return firestore_config

  @property
  def firestore_client(self) -> firestore.Client:
    if self._firestore_client is None:
      credentials_ad = credentials.ApplicationDefault()
      firebase_admin.initialize_app(credentials_ad)

      database_id = self.firestore_config['DATABASE_ID']

      self._logger.info(('Initializing Firestore client ',
                         f'[configuration={self.firestore_config}]'))

      self._firestore_client = firestore.client(database_id=database_id)

    return self._firestore_client
