import os
import re
import json
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

def conn_to_database():

    engine = create_engine('postgresql+psycopg2://' +
                           os.environ.get('POSTGRES_USER') + ':' +
                           os.environ.get('POSTGRES_PASSWORD') + '@' +
                           os.environ.get('POSTGRES_HOST') + ':5432/' +
                           os.environ.get('POSTGRES_DB'))

    return engine




def length_of_arg_check(args,key,permit_length):
    length_to_check = len(str(args[key]))
    return length_to_check==permit_length

def check_args(args, required=[], required_one_of=[], optional=[]):

    """Check arguments of GET request
    Args:
        args (dict): Arguments of GET request
        required (list): Names of required arguments
        required_one_of (list): Names of required arguments for which at least one is required
        optional (list): Names of optional arguments
    Returns:
        dict: http response compatible with json format along with modified args object
    """

    length_check_args_dict = {'date':6,'iso3code':3,'iso2code':2}
    status = 200
    message = ""

    # remove unused arguments
    args = {key: value for key, value in args.items() if key in required + required_one_of + optional}
    if not all(i in args.keys() for i in required):
        status = 400
        message = "Bad Request: All of these arguments are required {}.".format(required)
    elif len(required_one_of) > 0 and not any(i in args.keys() for i in required_one_of):
        status = 400
        message = "Bad Request: At least one of these arguments are required {}.".format(required_one_of)

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

def generate_sql(args,required_one_of):
    # args = {'iso2code':'AT'}

    # check the args
    # result = check_args(args, required=[], required_one_of=required_one_of, optional=[])
    # args = result.get('args')

    # if result['status'] == 200:
    # cols = ["date","country","iso3code","iso2code","ground_truth_internet_gg","internet_online_model_prediction","internet_online_offline_model_prediction","internet_offline_model_prediction","ground_truth_mobile_gg","mobile_online_model_prediction","mobile_online_offline_model_prediction","mobile_offline_model_prediction"]
    model_set = ["ground_truth_internet_gg","internet_online_model_prediction","internet_online_offline_model_prediction","internet_offline_model_prediction","ground_truth_mobile_gg","mobile_online_model_prediction","mobile_online_offline_model_prediction","mobile_offline_model_prediction"]
    table = 'dgg'

    # deal with the columns
    sql_query = "SELECT date,country,iso3code,iso2code,"

    if "model" in args.keys() and len(args['model'])>0:

        for key in set(args['model']).intersection(model_set):
            sql_query += f" {key},"

        if sql_query.endswith(","):
            sql_query = sql_query[:-1]
    else:
        sql_query = "SELECT *"

    sql_query += " FROM " + table + " WHERE "

    for key in set(args.keys()).intersection(["date","country","iso3code","iso2code"]):
        if key == 'date' and args != 'ALL':
            dates_string = str(args["date"]).replace("[","(").replace("]",")")
            sql_query += f"date IN {dates_string} AND "

            # sql_query += f"{key}={args[key]} AND "
        else:
            sql_query += f"{key}=\'{args[key]}\' AND "

    # if date is not in the args.keys() -> add date column in the sql_query

    sql_query = sql_query[:-5] + ';'
    return sql_query
    # else:
    #    return 'Internal Error'


def args_check_model(args):
    """
    update the model args in the query
    deal with 3 situations:
    1. "model" in the arg: find and store the elements that are intersected with the models list (full list)
    2. "model" in the arg but no element in the list -> update the args["model"] to the full model list
    3. no "model" in the arg  -> update the args["model"] to the full model list

    Returns: updated arg dict

    """
    models = ["ground_truth_internet_gg", "internet_online_model_prediction", "internet_online_offline_model_prediction", "internet_offline_model_prediction", "ground_truth_mobile_gg", "mobile_online_model_prediction", "mobile_online_offline_model_prediction", "mobile_offline_model_prediction"]

    if "model" in args.keys():
        models_found = re.findall("\"(\w+)\"", args['model'])
        args['model'] = list(set(models).intersection(models_found))
        if len(args['model']) ==0:
            args['model'] = models
    else:
        args["model"] = models
    return args

def args_check_date(args,conn):
    """
    update the model args in the query
    1. if there are date arg in the query
        restore the dates in the args that were stored as string into a list of numeric dates
    2. no date arg in the query:
        get the latest date as the arg

    """
    if "date" in args.keys():
        args["date"] = [int(x) for x in re.findall("(\d{6})", args['date'])]
        # TODO: check the date format
    else:
        sql = "SELECT max(date) FROM  dgg;"
        latest_date = int(pd.read_sql(sql, conn)['max'].values[0])
        args["date"] = [latest_date]
    return args


def reformat_json(df,args):
    """
    change the returned dataframe to the format that the frontend needs
    Args:
        args:
        df: dataframe returned from the read_sql
    """
    # dates check in the arg
    df['date'] = df['date'].apply(int)
    data = {}
    for iso2code in df["iso2code"].unique():
        date_dict = {}
        for date in df['date'].unique():
            model_dict = {}
            for model in args["model"]:
                try:
                    model_dict[model] = df.loc[(df['date'] == date) & (df['iso2code'] == iso2code)][model].values[0]
                except:
                    model_dict[model] = None
            date_dict[str(date)] = model_dict
        data[iso2code] = date_dict
    data = json.dumps(data)
    return data
