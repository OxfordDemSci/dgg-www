
import utils

def query_national(args):

    args = {'iso2code':'AT'}

    if len(args) > 0:
        result = utils.query_db(args)
        df = result.get('data').to_json(orient='columns')
        return df, result.get("status")
    else:
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments. See <a href='http://10.131.129.27/api/social-media-audience.html#query'>API documentation</a> for more info.", \
               400
