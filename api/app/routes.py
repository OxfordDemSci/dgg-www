from flask import request, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app import app, utils, endpoints



def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["DEBUG"] = False
    return app

app = create_app()


# define rate limiting
limiter = Limiter(app, key_func=get_remote_address)
rate_limit = "30/minute"


@app.route('/')
def home():
    return current_app.send_static_file('docs.html')


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 Error</h1><p>The resource could not be found.</p>", 404


@app.route('/init', methods=['GET'])
@limiter.limit(rate_limit)
def init():
    result = endpoints.init()
    return result


@app.route('/query_national', methods=['GET'])
@limiter.limit(rate_limit)
def query_national():
    args = dict(request.args)
    result = endpoints.query_national(args)
    return result



# query specific country
@app.route('/query_specific_country', methods=['GET'])
@limiter.limit(rate_limit)
def query_specific_country():
    args = dict(request.args)
    if len(args) > 0:
        result = endpoints.query_specific_country(args)
        return result['data'], result.get("status")
    else:
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments. See <a href='http://10.131.129.27/api/social-media-audience.html#query'>API documentation</a> for more info.", \
               400
