import os
import re
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()


# list of models (indicators)
models_desc = {
        'internet_online_model_prediction': {
            'name': 'Internet GG - Online',
            'type': 'internet',
            'order': 1,
            'description': 'Ratios of female-to-male internet use from our daily Facebook Gender Gap Index.'
                           '<br><strong>Coverage:</strong> Best<br>'
                           '<strong>Data Frequency:</strong> Daily<br>'
                           '<strong>Accuracy:</strong> Best'
        },
        'internet_online_offline_model_prediction': {
            'name': 'Internet GG - Combined',
            'type': 'internet',
            'order': 2,
            'description': 'Ratios of female-to-male internet use estimated using our daily Facebook Gender '
                           'Gap Index.<br>'
                           '<strong>Coverage:</strong> Moderate<br>'
                           '<strong>Data Frequency:</strong> Annual<br>'
                           '<strong>Accuracy:</strong> Good'
        },
        'internet_offline_model_prediction': {
            'name': 'Internet GG - Offline',
            'type': 'internet',
            'order': 3,
            'description': 'Ratios of female-to-male internet use estimated using only offline indicators on '
                           'the country’s development status (e.g. Human Development Index).<br>'
                           '<strong>Coverage:</strong> Moderate<br>'
                           '<strong>Data Frequency:</strong> Annual<br>'
                           '<strong>Accuracy:</strong> Low'
        },
        'ground_truth_internet_gg': {
            'name': 'Internet GG - ITU',
            'type': 'internet',
            'order': 4,
            'description': 'Ratios of female-to-male internet use from International Telecommunication Union '
                           '(ITU) statistics.<br>'
                           '<strong>Coverage:</strong> Lowest<br>'
                           '<strong>Data Frequency:</strong> Annual<br>'
                           '<strong>Accuracy:</strong> Observed survey data'
       },
        'mobile_online_model_prediction': {
            'name': 'Mobile GG - Online',
            'type': 'mobile',
            'order': 5,
            'description': 'Ratios of female-to-male mobile phone use from our Facebook Gender Gap Index.<br>'
                           '<strong>Coverage:</strong> Best<br>'
                           '<strong>Data Frequency:</strong> Daily<br>'
                           '<strong>Accuracy:</strong> Moderate'
        },
        'mobile_online_offline_model_prediction': {
            'name': 'Mobile GG - Combined',
            'type': 'mobile',
            'order': 6,
            'description': 'Ratios of female-to-male mobile phone use from our Facebook Gender '
                           'Gap Index and offline indicators (e.g Human Development Index).<br>'
                           '<strong>Coverage:</strong> Moderate<br>'
                           '<strong>Data Frequency:</strong> Annual<br>'
                           '<strong>Accuracy:</strong> Best'
        },
        'mobile_offline_model_prediction': {
            'name': 'Mobile GG - Offline',
            'type': 'mobile',
            'order': 7,
            'description': 'Ratios of female-to-male mobile phone use from offline indicators '
                           'such as the Human Development Index.<br>'
                           '<strong>Coverage:</strong> Moderate<br>'
                           '<strong>Data Frequency:</strong> Annual<br>'
                           '<strong>Accuracy:</strong> Moderate'
        },
        'ground_truth_mobile_gg': {
            'name': 'Mobile GG - GSMA',
            'type': 'mobile',
            'order': 8,
            'description': 'Ratios of female-to-male mobile phone use published by the Global System for Mobile '
                           'Communications Association (GSMA).<br>'
                           '<strong>Coverage:</strong> Lowest<br>'
                           '<strong>Data Frequency:</strong> Annual<br>'
                           '<strong>Accuracy:</strong> Observed survey data'
        }
    }


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

    length_check_args_dict = {'date': 6, 'iso3code': 3, 'iso2code': 2}
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

def generate_sql(args, date_type, required_one_of):
    # args = {'iso2code':'AT'}

    # check the args
    # result = check_args(args, required=[], required_one_of=required_one_of, optional=[])
    # args = result.get('args')

    # if result['status'] == 200:
    # cols = ["date", "country", "iso3code", "iso2code",
    #         "ground_truth_internet_gg", "internet_online_model_prediction",
    #         "internet_online_offline_model_prediction", "internet_offline_model_prediction",
    #         "ground_truth_mobile_gg", "mobile_online_model_prediction",
    #         "mobile_online_offline_model_prediction", "mobile_offline_model_prediction"]

    models = list(models_desc.keys())
    table = 'national'

    # deal with the columns
    sql_query = "SELECT date,country,iso3code,iso2code,"

    # model
    if "model" in args.keys() and len(args['model'])>0:

        for key in set(args['model']).intersection(models):
            sql_query += f" {key},"

        if sql_query.endswith(","):
            sql_query = sql_query[:-1]
    else:
        sql_query = "SELECT *"

    sql_query += " FROM " + table + " WHERE "

    for key in set(args.keys()).intersection(["date", "country", "iso3code", "iso2code"]):
        if key == 'date' and args != 'ALL':
            if date_type == "range":
                sql_query += f" date >= {args['date'][0]} and date <= {args['date'][1]} AND "
            if date_type == "list":
                dates_string = str(args["date"]).replace("[","(").replace("]",")")
                sql_query += f"date IN {dates_string} AND "

            # sql_query += f"{key}={args[key]} AND "
        else:
            sql_query += f"{key}=\'{args[key]}\' AND "

    # if date is not in the args.keys() -> add date column in the sql_query
    if sql_query.endswith(' AND '):
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

    models = list(models_desc.keys())

    if "model" in args.keys():
        models_found = re.findall("\"(\w+)\"", args['model'])
        args['model'] = list(set(models).intersection(models_found))
        if len(args['model']) ==0:
            args['model'] = models
    else:
        args["model"] = models
    return args

def args_check_date(args, conn):
    """
    update the model args in the query
    1. if there are date arg in the query
        restore the dates in the args that were stored as string into a list of numeric dates
    2. no date arg in the query:
        get the latest date as the arg

    """
    table = 'national'
    if "date" in args.keys():
        args["date"] = [int(x) for x in re.findall("(\d{6})", args['date'])]
        # TODO: check the date format
    else:
        sql = "SELECT max(date) FROM " + table + ";"
        latest_date = int(pd.read_sql(sql, conn)['max'].values[0])
        args["date"] = [latest_date]
    return args


def reformat_json(df, args):
    """
    change the returned dataframe to the format that the frontend needs
    Args:
        args:
        df: dataframe returned from the read_sql
    """
    # dates check in the arg
    df['date'] = df['date'].apply(int)
    df.fillna(-999, inplace=True)
    data = {}
    for iso2code in df["iso2code"].unique():
        date_dict = {}
        for date in df['date'].unique():
            model_dict = {}
            for model in args["model"]:
                try:
                    model_dict[model] = df.loc[(df['date'] == date) & (df['iso2code'] == iso2code)][model].values[0]
                    # if np.isnan(model_dict[model]): model_dict[model] = None
                    if model_dict[model] == -999: model_dict[model] = None
                except:
                    model_dict[model] = None
            date_dict[str(date)] = model_dict
        data[iso2code] = date_dict
    return data

def palette(n=6):
    """
    Color palette for mapping results.

    Parameters:
        n (int): Number of colors in palette. Must be 6, 8, or 10.

    Returns:
        pal (dict): Color palette with hex codes and break points

    """

    # ---- color ramp ---- #
    colors = ["#e76254",  # dark red
              "#ef8a47",
              "#f7aa58",
              "#ffd06f",
              "#ffe6b7",  # light red
              "#aadce0",  # light blue
              "#72bcd5",
              "#528fad",
              "#376795",
              "#1e466e"  # dark blue
              ]

    if n not in [4, 6, 8, 10]:
        n = 6

    if n == 4:
        colors = [colors[i] for i in [0, 2, 7, 9]]
    elif n == 6:
        colors = [colors[i] for i in [0, 1, 3, 5, 6, 8]]
    elif n == 8:
        colors = [colors[i] for i in [0, 1, 3, 4, 5, 6, 8, 9]]

    # ---- breaks (modified from GISRede's function) ---- #
    models = list(models_desc.keys())

    conn = conn_to_database()

    table = 'national'
    sql = 'SELECT DISTINCT date FROM ' + table + ';'
    data = pd.read_sql(sql, conn)

    latest_date = str(int(max(data['date'])))

    sql = 'SELECT ' + ",".join(models) + ' FROM ' + table + ' WHERE date = ' + latest_date + ';'
    df = pd.read_sql(sql, conn)

    breaks = {}
    labels = {}
    for model in models:
        x = df[model]
        x = x[x > -999]

        b = [None] * (n + 1)
        b[0] = 0
        b[len(b)-1] = 1.0  # float('inf')
        b[int(n/2)] = np.median(x)
        for i in range(1, int(n/2)):
            b[i] = np.quantile(a=x[x < np.median(x)], q=i * (2 / n))
            b[i+int(n/2)] = np.quantile(a=x[x > np.median(x)], q=i * (2 / n))

        breaks[model] = b

        # bin labels for legend
        rnd = 3
        lab = [None] * (len(b) - 1)
        for i in range(len(b)-1):
            if i == 0:
                lab[i] = str(format(round(np.min(x), rnd), '.' + str(rnd) + 'f')) + '-' + \
                         str(format(round(b[i + 1], rnd) - 0.001, '.' + str(rnd) + 'f'))
            elif i < (len(b) - 2):
                lab[i] = str(format(round(b[i], rnd), '.' + str(rnd) + 'f')) + '-' + \
                         str(format(round(b[i + 1], rnd) - 0.001, '.' + str(rnd) + 'f'))
            else:
                lab[i] = str(format(round(b[i], rnd), '.' + str(rnd) + 'f')) + '-Above'

        labels[model] = lab

    pal = {
        "title": "Internet/Mobile Gender Gap (Women:Men)",
        "subtitles": ["Less Equality", "More Equality"],
        "colors": colors,
        "breaks": breaks,
        "labels": labels
    }

    return pal

