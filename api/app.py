import time
from flask import Flask, request, jsonify
import utils
from docker.api import  endpoints
app = Flask(__name__)


@app.route('/') # why get here?
def home():
    return '''<h1>Leverhulme Center for Demographic Science</h1>
<p>A prototype API (v1) to infuse data science into demography.</p>'''

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 Error</h1><p>The resource could not be found.</p>", 404

# test page to query the database
@app.route('/db_test',methods=['GET'])
def query():
    args = dict(request.args)
    if len(args) > 0:
        result = utils.query_db(args)
        df = result.get('data').to_dict()
        return df, result.get("status")
    else:
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments. See <a href='http://10.131.129.27/api/social-media-audience.html#query'>API documentation</a> for more info.", \
               400
@app.route('/initial',methods=['GET'])
def query_national():
    args = dict(request.args)
    result = endpoints.query_national(args)
    return result
if __name__ == '__main__':
    app.run()
