import utils
import pandas as pd

def init():

    result = {}

    conn = utils.conn_to_database()

    # list models
    sql = 'SELECT * FROM dgg LIMIT 0;'
    data = pd.read_sql(sql, conn)
    result['models'] = list(data.columns[4:])

    # list countries with national-level data
    sql = 'SELECT DISTINCT iso2code FROM dgg;'
    data = pd.read_sql(sql, conn)
    result['countries'] = data['iso2code'].tolist()

    # list dates with data
    sql = 'SELECT DISTINCT date FROM dgg;'
    data = pd.read_sql(sql, conn)
    result['dates'] = data['date'].tolist()
    result['dates'] = [int(x) for x in result['dates']]

    # blurb
    result['blurb'] = 'Yodel ay he hooo!'

    # contact
    result['contact'] = 'info@digitalgendergaps.org'

    return result


def query_national(args):

    # args = {'iso2code':'AT'}

    if len(args) == 0:
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments.", \
               400
    else:
        result = utils.query_db(args)
        df = result.get('data').to_json(orient='columns')
        return df, result.get("status")
