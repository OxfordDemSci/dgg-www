# import numpy as np
# import csv
# from src import params
# from io import StringIO

from psycopg2 import connect
import pandas as pd

def conn_to_database():
    conn = connect(
        dbname="dggpanel",
        user="postgres",
        host="localhost", #10.131.129.27
        password="dgg"
    )
    cursor = conn.cursor()
    return conn, cursor


def length_of_arg_check(args,key,permit_length):
    length_to_check = len(str(args[key]))
    return length_to_check==permit_length

def check_args(args, required=[], required_oneof=[], optional=[]):

    """Check arguments of GET request
    Args:
        args (dict): Arguments of GET request
        required (list): Names of required arguments
        required_oneof (list): Names of required arguments for which at least one is required
        optional (list): Names of optional arguments
    Returns:
        dict: http response compatible with json format along with modified args object
    """

    length_check_args_dict = {'date':6,'iso3code':3,'iso2code':2}
    status = 200
    message = ""

    # remove unused arguments
    args = {key: value for key, value in args.items() if key in required + required_oneof + optional}
    if not all(i in args.keys() for i in required):
        status = 400
        message = "Bad Request: All of these arguments are required {}.".format(required)
    elif len(required_oneof) > 0 and not any(i in args.keys() for i in required_oneof):
        status = 400
        message = "Bad Request: At least one of these arguments are required {}.".format(required_oneof)

    # check length of data
    for key in length_check_args_dict.keys():
        if key in args.keys():
            if not length_of_arg_check(args=args, key=key, permit_length=length_check_args_dict[key]):
                status = 400
                message = f"Bad Request: length of '{key}' must be {length_check_args_dict[key]}"
    # deal with date
    if 'date' in args.keys():

        if not isinstance(args.get('date'), int):
            try:
                args['date'] = int(args['date'])
            except:
                status = 400
                message = "Bad Request: '{}' cannot be coerced to a int data YYYY-MM.".format(args['date'])
        else:
            args['date'] = 'ALL'  # all available dates

    return {'status': status,'message': message, "args": args}


# test zone

def query_db(args):
    # check the args
    result = check_args(args, required=[], required_oneof=['iso3code', 'iso2code', 'country'], optional=[])
    args = result.get('args')


    if result['status'] == 200:
        cols = ["date","country","iso3code","iso2code","ground_truth_internet_gg","internet_online_model_prediction","internet_online_offline_model_prediction","internet_offline_model_prediction","ground_truth_mobile_gg","mobile_online_model_prediction","mobile_online_offline_model_prediction","mobile_offline_model_prediction"]
        table = 'dgg'
        sql_query = "SELECT * FROM " + table + " WHERE "
        for key in set(args.keys()).intersection(["date","country","iso3code","iso2code"]):
            if key == 'date':
                if not args[key] == 'ALL':
                    sql_query += f"{key}={args[key]} AND "
            else:
                sql_query += f"{key}=\'{args[key]}\' AND "

        sql_query = sql_query[:-5] + ';'
        print(sql_query)
    try:
        conn, cursor = conn_to_database()
        data = pd.read_sql(sql_query, conn,index_col=['date'])

        message = 'OK: Data successfully selected from database.'
        status = 200
    except:
        data = pd.DataFrame()
        status = 500
        message = 'Internal Server Error: Error returned from PostgreSQL server on SELECT.'
    return {'data': data, "status": status, 'message': message}

