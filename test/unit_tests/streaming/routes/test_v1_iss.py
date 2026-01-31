''' Module to test v1 based routing. '''
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.streaming.middleware.iss_controller import V1ISSController
from src.streaming.routes.v1_iss import create_v1_blueprint


class V1ISSRoutingTestSuite(TestCase):
  ''' Unit test suite for v1 based routing. '''

  def setUp(self):
    self._controller: V1ISSController = MagicMock(spec=V1ISSController)

  @patch(target='src.streaming.routes.v1_iss.ServerSentEventsBlueprint')
  def test_should_add_correct_prefix_to_v1_blueprint(
      self, blueprint: MagicMock) -> None:
    create_v1_blueprint(controller=self._controller)

    blueprint.assert_called_with('v1_blueprints',
                                 'src.streaming.routes.v1_iss',
                                 url_prefix='/v1')
