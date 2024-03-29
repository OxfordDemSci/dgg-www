from flask import request, current_app, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app import app, endpoints


# define rate limiting
limiter = Limiter(app,
                  key_func=get_remote_address,
                  # application_limits=['60/minute', '1000/hour', '10000/day'],
                  default_limits=['60/minute', '1000/hour', '10000/day'],
                  strategy='fixed-window-elastic-expiry',
                  storage_uri="memcached://dgg_memcached:11211",
                  storage_options={}
                  )


@app.route('/')
def home():
    return current_app.send_static_file('docs.html')


@app.errorhandler(404)
def page_not_found(e):
    return f"<h1>404 Error</h1><p>The resource could not be found. {e}</p>", 404


@app.route('/init', methods=['GET'])
def init():
    result = endpoints.init()
    return jsonify(result), result.get('status')


@app.route('/query_national', methods=['GET'])
def query_national():
    args = dict(request.args)
    if len(args) == 0:
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments. " \
               "See <a href='./'>API documentation</a> for more information.", \
               400
    else:
        result = endpoints.query_national(args)
        return jsonify(result), result.get('status')


@app.route('/query_specific_country', methods=['GET'])
def query_specific_country():
    args = dict(request.args)
    if len(args) == 0:
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments. " \
               "See <a href='./'>API documentation</a> for more information.", \
               400
    else:
        result = endpoints.query_specific_country(args)
        return jsonify(result), result.get('status')


@app.route('/download_data_with_dates', methods=['GET'])
def download_data_with_dates():
    args = dict(request.args)
    if len(args) == 0:
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments. " \
               "See <a href='./'>API documentation</a> for more information.", \
               400
    else:
        result = endpoints.download_data_with_dates(args)
        return jsonify(result), result['status']


@app.route('/write_national', methods=['GET'])
@limiter.exempt
def write_national():
    args = dict(request.args)
    if len(args) == 0:
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments. " \
               "See <a href='./'>API documentation</a> for more information.", \
               400
    else:
        result = endpoints.write_national(args)
        return jsonify(result), result['status']
