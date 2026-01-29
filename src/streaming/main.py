# pylint: disable=redefined-outer-name
'''
  Module using Flask SSE for streaming events to connected clients.
'''
import logging

from cfg_environ.config import Config, ConfigFacade
from flask import Flask
from iss_location_client.client import (ISSLocationClient,
                                        ISSLocationFirestoreClient)

from .client.subscriber.client import RedisSubscriberClient, SubscriberClient
from .middleware.iss_controller import V1ISSController
from .middleware.iss_repository import ISSPassThroughRepository, ISSRepository
from .util.event_handling import on_iss_location_update


def configure_logging() -> None:
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s %(levelname)s %(name)s: %(message)s')


def get_config() -> Config:
  config = ConfigFacade(config_path=CONFIG_PATH,
                        config_env=CONFIG_ENV,
                        config_env_default=CONFIG_ENV_DEFAULT)

  return config


def get_iss_client(config: Config) -> ISSLocationClient:
  client = ISSLocationFirestoreClient(config=config)

  return client


def get_iss_repository(client: ISSLocationClient) -> ISSRepository:
  repository = ISSPassThroughRepository(client=client)

  return repository


def get_v1_controller(repository: ISSRepository,
                      config: Config) -> V1ISSController:
  controller = V1ISSController(repository=repository, config=config)

  return controller


def get_subscriber(handler, config: Config) -> SubscriberClient:
  redis_subscriber = RedisSubscriberClient(config=config)
  redis_subscriber.subscribe_iss_location(handler=handler)

  return redis_subscriber


def get_flask_app(config: Config) -> Flask:
  app = Flask(__name__)
  # We are not running this application on the bridge network.
  # A user-managed Docker network was created to make testing locally with
  # a redis instance easier.
  redis_url = config.read_dict('FLASK_SSE')
  app.config[FLASK_SSE_REDIS_URL_KEY] = redis_url

  return app


CONFIG_PATH = 'src/streaming/config'
CONFIG_ENV = 'development'
CONFIG_ENV_DEFAULT = 'default'

FLASK_SSE_REDIS_URL_KEY = 'REDIS_URL'

configure_logging()
config = get_config()
client = get_iss_client(config=config)
iss_repository = get_iss_repository(client=client)
v1_controller = get_v1_controller(repository=iss_repository, config=config)
subscriber = get_subscriber(handler=on_iss_location_update, config=config)
app = get_flask_app(config=config)
