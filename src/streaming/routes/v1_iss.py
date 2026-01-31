''' Module handling v1 based routing '''
import json

from flask import Blueprint, Response, request
from flask_sse import ServerSentEventsBlueprint

from ..middleware.iss_controller import V1ISSController


def create_v1_blueprint(controller: V1ISSController) -> Blueprint:
  v1_blueprint = ServerSentEventsBlueprint('v1_blueprints',
                                           __name__,
                                           url_prefix='/v1')

  @v1_blueprint.route('/iss/location', methods=['GET'])
  def get_events():
    window = request.args.get('window')
    events = controller.v1_iss_events(window=window)
    response_json = json.dumps(events)
    status = 200
    response = Response(response=response_json, status=status)

    return response

  v1_blueprint.add_url_rule(rule='/iss/stream',
                            endpoint='_iss_stream',
                            view_func=v1_blueprint.stream)

  return v1_blueprint
