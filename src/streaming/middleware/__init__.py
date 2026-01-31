''' Init for middleware package. '''

from cfg_environ.config import Config
from iss_location_client.client import ISSLocationClient

from .iss_controller import V1ISSController
from .iss_repository import ISSPassThroughRepository, ISSRepository


def get_v1_controller(repository: ISSRepository,
                      config: Config) -> V1ISSController:
  controller = V1ISSController(repository=repository, config=config)

  return controller


def get_iss_repository(client: ISSLocationClient) -> ISSRepository:
  repository = ISSPassThroughRepository(client=client)

  return repository
