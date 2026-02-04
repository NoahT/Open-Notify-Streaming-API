''' Module handling v1 based routing '''
from flask import Blueprint, request
from flask_sse import ServerSentEventsBlueprint
from werkzeug.exceptions import HTTPException

from ..middleware.iss_controller import V1ISSController


def create_v1_blueprint(controller: V1ISSController) -> Blueprint:
  v1_blueprint = ServerSentEventsBlueprint('v1_blueprints',
                                           __name__,
                                           url_prefix='/v1')

  @v1_blueprint.route('/iss/location', methods=['GET'])
  def get_events():
    window = request.args.get('window', default=30, type=int)
    response = controller.v1_iss_events(window=window)
    return response

  @v1_blueprint.errorhandler(HTTPException)
  def error_handler(exception: HTTPException):
    response_json = {
        'description': exception.description,
        'message': exception.response
    }

    return (response_json, exception.code)

  v1_blueprint.add_url_rule(rule='/iss/stream',
                            endpoint='_iss_stream',
                            view_func=v1_blueprint.stream)

  return v1_blueprint
