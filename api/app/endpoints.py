from app import utils
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
    # args = {'iso2code': 'AT'}
    conn = utils.conn_to_database()
    result = {}
    if len(args) == 0:
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments.", 400
    else:
        sql = utils.generate_sql(args)
        result['data'] = pd.read_sql(sql, conn)
        result['status'] = 200
        return result

def query_specific_country(args):
    conn = utils.conn_to_database()
    result = {}
    if len(args) == 0:
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments.", 400
    elif len(args) == 1:
        sql = utils.generate_sql(args)

        # dates
        data = pd.read_sql(sql, conn)
        data['date'] = data['date'].apply(int)
        result['data'] = data.to_dict()

        for colname in ['country','iso3code','iso2code']:
            result['data'] = utils.rewrite_country_name_dict(result['data'], colname)

        result['status'] = 200
        return result
    else:
        # TODO: do we need to allow multiple country query here?
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments."


# data = pd.read_csv('/Users/valler/Python/RA/Gender_Inequality/dgg-www/sql/initial_data/mau_upper_monthly_model_2_2022-06.csv')





