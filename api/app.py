
from flask import Flask, request, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import utils, endpoints
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["DEBUG"] = False
    return app

app = create_app()

limiter = Limiter(app, key_func=get_remote_address)
rate_limit = "30/minute"

@app.route('/') # why get here?
def home():
    return current_app.send_static_file('docs.html')

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 Error</h1><p>The resource could not be found.</p>", 404

@app.route('/init',methods=['GET'])
@limiter.limit(rate_limit)
def init():
    result = endpoints.init()
    return result

@app.route('/query_national',methods=['GET'])
@limiter.limit(rate_limit)
def query_national():
    args = dict(request.args)
    result = endpoints.query_national(args)
    return result

# test page to query the database
@app.route('/db_test',methods=['GET'])
@limiter.limit(rate_limit)
def query():
    args = dict(request.args)
    if len(args) > 0:
        result = utils.query_db(args)
        df = result.get('data').to_dict()
        return df, result.get("status")
    else:
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments. See <a href='http://10.131.129.27/api/social-media-audience.html#query'>API documentation</a> for more info.", \
               400


