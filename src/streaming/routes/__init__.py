''' Init for routes package. '''
import logging

from cfg_environ.config import Config
from flask import Flask
from flask_sse import sse

from ..middleware.iss_controller import V1ISSController
from .v1_iss import create_v1_blueprint

FLASK_SSE_REDIS_URL_KEY = 'REDIS_URL'
LOGGER = logging.getLogger(__name__)


def get_flask_app(controller: V1ISSController, config: Config) -> Flask:
  app = Flask(__name__)
  app.register_blueprint(create_v1_blueprint(controller=controller))
  # We are not running this application on the bridge network.
  # A user-managed Docker network was created to make testing locally with
  # a redis instance easier.
  redis_url = config.read_dict('FLASK_SSE')['REDIS_URL']
  app.config[FLASK_SSE_REDIS_URL_KEY] = redis_url

  return app


def on_iss_location_update(message: dict) -> None:
  channel = message['channel']
  data = message['data']
  sse.publish(data, type='iss_location')
  LOGGER.info('Published ISS location update [channel=%s, data=%s]', channel,
              data)
