''' Module handling v1 based routing '''
from flask import request

from ..main import app, v1_controller


@app.route('/v1/iss/events', methods=['GET'])
def get_events():
  window = request.args.get('window')
  return v1_controller.v1_iss_events(window=window)
