import os
import re
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from ast import literal_eval
from dotenv import load_dotenv
load_dotenv()


# list of models (indicators)
models_desc = {
        'ground_truth_internet_gg': {
            'name': 'Internet GG - ITU',
            'type': 'internet',
            'description': '<strong>Description:</strong> Ratios of female-to-male internet use from International '
                           'Telecommunication Union (ITU).<br>'
                           '<strong>Data Frequency:</strong> Annual<br>'
                           '<strong>Coverage:</strong> Lowest<br>'
                           '<strong>Accuracy:</strong> Best'
        },
        'internet_online_model_prediction': {
            'name': 'Internet GG - Online',
            'type': 'internet',
            'description': '<strong>Description:</strong> Ratios of female-to-male internet use from our daily Facebook '
                           'Gender Gap Index.<br>'
                           '<strong>Data Frequency:</strong> Daily<br>'
                           '<strong>Coverage:</strong> Best<br>'
                           '<strong>Accuracy:</strong> Very good'
        },
        'internet_offline_model_prediction': {
            'name': 'Internet GG - Offline',
            'type': 'internet',
            'description': '<strong>Description:</strong> Ratios of female-to-male internet use estimated using only '
                           'offline indicators (e.g. Human Development Index).<br>'
                           '<strong>Data Frequency:</strong> Annual<br>'
                           '<strong>Coverage:</strong> Moderate<br>'
                           '<strong>Accuracy:</strong> Low'
        },
        'internet_online_offline_model_prediction': {
            'name': 'Internet GG - Combined',
            'type': 'internet',
            'description': '<strong>Description:</strong> Ratios of female-to-male internet use estimated using our '
                           'daily Facebook Gender Gap Index combined with offline indicators.<br>'
                           '<strong>Data Frequency:</strong> Annual<br>'
                           '<strong>Coverage:</strong> Moderate<br>'
                           '<strong>Accuracy:</strong> Good'
        },
        'ground_truth_mobile_gg': {
            'name': 'Mobile GG - GSMA',
            'type': 'mobile',
            'description': '<strong>Description:</strong> Ratios of female-to-male mobile phone use published by the '
                           'Global System for Mobile Communications Association (GSMA).<br>'
                           '<strong>Data Frequency:</strong> Annual<br>'
                           '<strong>Coverage:</strong> Lowest<br>'
                           '<strong>Accuracy:</strong> Best'
        },
        'mobile_online_model_prediction': {
            'name': 'Mobile GG - Online',
            'type': 'mobile',
            'description': '<strong>Description:</strong> Ratios of female-to-male mobile phone use from our Facebook '
                           'Gender Gap Index.<br>'
                           '<strong>Data Frequency:</strong> Daily<br>'
                           '<strong>Coverage:</strong> Best<br>'
                           '<strong>Accuracy:</strong> Moderate'
        },
        'mobile_offline_model_prediction': {
            'name': 'Mobile GG - Offline',
            'type': 'mobile',
            'description': '<strong>Description:</strong> Ratios of female-to-male mobile phone use from offline '
                           'indicators such as the Human Development Index.<br>'
                           '<strong>Data Frequency:</strong> Annual<br>'
                           '<strong>Coverage:</strong> Moderate<br>'
                           '<strong>Accuracy:</strong> Moderate'
        },
        'mobile_online_offline_model_prediction': {
            'name': 'Mobile GG - Combined',
            'type': 'mobile',
            'description': '<strong>Description:</strong> Ratios of female-to-male mobile phone use from our Facebook '
                           'Gender Gap Index and offline indicators (e.g Human Development Index).<br>'
                           '<strong>Data Frequency:</strong> Annual<br>'
                           '<strong>Coverage:</strong> Moderate<br>'
                           '<strong>Accuracy:</strong> Very good'
        }
}


def conn_to_database(mode='r'):

    if mode == 'w':
        user = 'dgg_writer'
        pw = os.environ.get('POSTGRES_WPASS')
    else:
        user = 'dgg_reader'
        pw = os.environ.get('POSTGRES_RPASS')

    engine = create_engine('postgresql+psycopg2://' + \
                           user + ':' + \
                           pw + '@' + \
                           os.environ.get('POSTGRES_HOST') + '/' + \
                           os.environ.get('POSTGRES_DB'))

    return engine


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

    length_args = {'date': 6, 'start_date': 6, 'end_date': 6, 'iso2code': 2, 'iso2': 2}
    int_args = ['date', 'start_date', 'end_date']
    str_args = ['iso2code', 'iso2', 'token']
    list_args = ['model']
    float_args = list(models_desc.keys())
    bool_args = ['pretty_names']

    status = 200
    message = ""

    # remove unused arguments
    args = {key: value for key, value in args.items() if key in required + required_one_of + optional}
    if not all(i in args.keys() for i in required):
        status = 400
        message = "Bad Request: All of these arguments are required: {}.".format(', '.join(required))
    elif len(required_one_of) > 0 and not any(i in args.keys() for i in required_one_of):
        status = 400
        message = "Bad Request: At least one of these arguments is required: {}.".format(', '.join(required_one_of))

    # ---- check data types ---- #

    # string
    if status == 200:
        for key in set(args.keys()).intersection(str_args):
            try:
                args[key] = str(args[key])
                if not isinstance(args.get(key), str):
                    raise TypeError()
            except:
                status = 400
                message = f"Bad Request: '{key}' cannot be coerced to str."

    # validate token
    if status == 200 and 'token' in args.keys():
        if args.get('token') == os.environ.get('WRITE_TOKEN'):
            args.pop('token')
        else:
            status = 401
            message = 'Bad Request: Unauthorized for write access.'

    # int
    if status == 200:
        for key in set(args.keys()).intersection(int_args):
            try:
                args[key] = int(args[key])
                if not isinstance(args.get(key), int):
                    raise TypeError()
            except:
                status = 400
                message = f"Bad Request: '{key}' cannot be coerced to int."

    # float
    if status == 200:
        for key in set(args.keys()).intersection(float_args):
            try:
                args[key] = float(args[key])
                if not isinstance(args.get(key), float):
                    raise TypeError()
            except:
                status = 400
                message = f"Bad Request: '{key}' cannot be coerced to float."

    if status == 200:
        for key in set(args.keys()).intersection(bool_args):
            try:
                if isinstance(args.get(key), str):
                    args[key] = args.get(key).lower()
                if args.get(key) in [True, 1, 'true', 't', 'yes', 'y', 'on']:
                    args[key] = True
                elif args.get(key) in [False, 0, 'false', 'f', 'no', 'n', 'off']:
                    args[key] = False
                else:
                    args[key] = True
                if not isinstance(args.get(key), bool):
                    raise TypeError()
            except:
                status = 400
                message = f"Bad Request: '{key}' cannot be coerced to boolean."

    # list
    if status == 200:
        for key in set(args.keys()).intersection(list_args):
            if not isinstance(args.get(key), list):
                try:
                    if args[key][0] == '[':
                        args[key] = list(literal_eval(args[key]))
                    else:
                        args[key] = [args[key]]
                    if not isinstance(args.get(key), list):
                        raise TypeError()
                except:
                    status = 400
                    message = f"Bad Request: '{key}' could not be coerced to a list."

    # ---- check length ---- #
    if status == 200:
        for key in length_args.keys():
            if key in args.keys():
                if not len(str(args[key])) == length_args[key]:
                    status = 400
                    message = f"Bad Request: Length of '{key}' must be {length_args[key]}."

    # ----  check model list ---- #
    if status == 200:
        if 'model' in args.keys():

            args['model'] = list(set(args['model']).intersection(models_desc.keys()))

            if len(args['model']) == 0:
                args['model'] = list(models_desc.keys())

            if not isinstance(args.get('model'), list):
                status = 400
                message = "Bad Request: 'model' argument must be a list."

    return {'status': status, 'message': message, 'args': args}


def reformat_json(df):
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
    for iso2code in df["iso2"].unique():
        date_dict = {}
        for date in df['date'].unique():
            model_dict = {}
            for model in [x for x in df.columns if x not in ['date', 'iso2', 'iso3', 'name']]:
                try:
                    model_dict[model] = df.loc[(df['date'] == date) & (df['iso2'] == iso2code)][model].values[0]
                    # if np.isnan(model_dict[model]): model_dict[model] = None
                    if model_dict[model] == -999:
                        model_dict[model] = None
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

        break_type = 'fixed'

        if break_type == 'fixed':

            if n == 4:
                b = [0, 0.80, 0.90, 0.99, 1]
            elif n == 6:
                b = [0, 0.75, 0.85, 0.90, 0.95, 0.99, 1]
            elif n == 8:
                b = [0, 0.75, 0.80, 0.85, 0.90, 0.93, 0.96, 0.99, 1]
            elif n == 10:
                b = [0, 0.70, 0.75, 0.80, 0.85, 0.90, 0.92, 0.94, 0.96, 0.99, 1]

        elif break_type == 'quantiles':

            b[0] = 0
            b[len(b) - 1] = 1.0  # float('inf')
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
        "title": "Digital Gender Gap",
        "subtitles": ["Less Equality<br><em>female-to-male</em>", "More Equality"],
        "colors": colors,
        "breaks": breaks,
        "labels": labels
    }

    return pal

