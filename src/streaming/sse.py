from flask import Flask, render_template
from flask_sse import sse

# For now, the scaffolding/boilerplate uses the sample code on Flask-SSE
# documentation https://flask-sse.readthedocs.io/en/latest/quickstart.html.
# We will update this once the boilerplate is set up.

app = Flask(__name__)
# We are not running this sample application on the bridge network.
# A user-managed Docker network was created to make testing locally with
# a redis instance easier.
app.config['REDIS_URL'] = 'redis://redis:6379'
app.register_blueprint(sse, url_prefix='/stream')


@app.route('/')
def index():
  return render_template('./index.html')


@app.route('/hello')
def publish_hello():
  sse.publish({'message': 'Hello!'}, type='greeting')
  return 'Message sent!'
