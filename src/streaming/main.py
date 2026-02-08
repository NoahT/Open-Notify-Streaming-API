# pylint: disable=redefined-outer-name
'''
  Module using Flask SSE for streaming events to connected clients.
'''
from .client import get_iss_client
from .config import get_config
from .middleware import get_iss_repository, get_v1_controller
from .routes import get_flask_app

config = get_config()
client = get_iss_client(config=config)
iss_repository = get_iss_repository(client=client)
v1_controller = get_v1_controller(repository=iss_repository, config=config)
app = get_flask_app(controller=v1_controller, config=config)
