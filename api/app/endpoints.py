from app import utils
import pandas as pd
from flask import jsonify
import re

def init():
    result = {}

    conn = utils.conn_to_database()

    # list models
    sql = 'SELECT * FROM dgg LIMIT 0;'
    data = pd.read_sql(sql, conn)
    result['models'] = list(data.columns[4:])

    # list countries with national-level data
    sql = 'SELECT DISTINCT iso2code,country FROM dgg;'
    data = pd.read_sql(sql, conn)
    result['countries'] = [{"iso2code":x,"country":y} for x,y in zip(data['iso2code'],data["country"])]

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

# args={"iso2code":"AT"}

def query_specific_country(args):
    """
    query the database for one country at one time
    - requires
    valid query examples:
    1. iso2code=AT&model=["ground_truth_mobile_gg"]

    Returns:

    """
    conn = utils.conn_to_database()
    result = {}

    args = utils.args_check_model(args)
    sql = utils.generate_sql(args, required_one_of=['iso3code', 'iso2code', 'country'])
    # update the sql sentence with date arg

    df = pd.read_sql(sql, conn)
    # post-process the json
    result['data'] = df.to_dict()
    data = utils.reformat_json(df=df, args=args)

    result['data'] = data
    result['status'] = 200
    return result


# data = pd.read_csv('/Users/valler/Python/RA/Gender_Inequality/dgg-www/sql/initial_data/mau_upper_monthly_model_2_2022-06.csv')

# utils.generate_sql(args=)
# args = {"model":'["ground_truth_internet_gg","internet_online_model_prediction"]',"date":'[202207,202206]'}
# args = {"date":'[202207,202206]'}


def query_national(args):
    # TODO: Better Error handle
    # date must be list or empty
    conn = utils.conn_to_database()
    result = {}

    # check the args
    # first check the model
    args = utils.args_check_model(args)
    args = utils.args_check_date(args, conn)

    # generate sql
    sql = utils.generate_sql(args, required_one_of=[])
    df = pd.read_sql(sql, conn)

    result['data'] = utils.reformat_json(df=df, args=args)
    result['status'] = 200

    return result


"""
pd.read_sql(sql_query, conn)

conn = create_engine('postgresql+psycopg2://'+
                           "postgres" + ':' +
                           "dgg" + '@' +
                           "localhost"+ ':5432/' +
                           "dggpanel")
args = args_check_model(args)
args = args_check_date(args,conn)
sql = generate_sql(args, required_one_of=[])


"""

sql = "SELECT DISTINCT iso2code,country FROM dgg;"
df=pd.read_sql(sql, conn)
