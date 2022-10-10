from app import utils
import pandas as pd

def init():
    """
    API endpoint to initialize the front end

    Parameters:
        None

    Returns:
        result (dict): Contains a list of models (indicators), countries, dates with data, blurb, and contact.
    """

    result = {}

    conn = utils.conn_to_database()

    # list model types
    result['types'] = ['internet', 'mobile']

    # list models
    result['models'] = utils.models_desc

    # list countries with national-level data
    table = 'national'
    sql = 'SELECT DISTINCT iso2code,country FROM ' + table + ';'
    data = pd.read_sql(sql, conn)
    result['countries'] = [{"iso2code": x, "country": y} for x, y in zip(data['iso2code'], data["country"])]

    # list dates with data
    sql = 'SELECT DISTINCT date FROM ' + table + ';'
    data = pd.read_sql(sql, conn)
    result['dates'] = data['date'].tolist()
    result['dates'] = [int(x) for x in result['dates']]

    # color palette
    result['palette'] = utils.palette(n=6)

    # contact
    result['contact'] = 'digitalgendergaps@gmail.com'

    return result


def query_specific_country(args):
    """
    API endpoint to query the database for one country at one time

    Parameters:
        args (dict): A dictionary containing items str:iso2code and/or list:model

    Examples:
        - args = {"iso2code": "AT"}
        - args = {"iso2code": "AT", "model": ["ground_truth_mobile_gg"]}

    Returns:
        result (dict): Contains a list of models (indicators), countries, dates with data, blurb, and
        contact email.
    """

    conn = utils.conn_to_database()
    result = {}

    args = utils.args_check_model(args)
    sql = utils.generate_sql(args, date_type='list', required_one_of=['iso3code', 'iso2code', 'country'])
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
    """
    API endpoint to query the database for all countries

    Parameters:
        args (dict): A dictionary containing items ??

    Examples:
        - ??

    Returns:
        result (json): Data
    """

    # TODO: Better Error handle
    # date must be list or empty

    conn = utils.conn_to_database()
    result = {}

    # check the args
    args = utils.args_check_model(args)
    args = utils.args_check_date(args, conn)

    # generate sql
    sql = utils.generate_sql(args, date_type='list', required_one_of=[])
    df = pd.read_sql(sql, conn)

    result['data'] = utils.reformat_json(df=df, args=args)
    result['status'] = 200

    return result


def download_data_with_dates(args={}):
    """
    Enable the download function to download data by 2 dates (start dates and end dates)

    Parameters:
        args (dict): A dictionary containing items: "date"

    Examples:
        - args = {}
        - args = {"date":'[202202, 202207]'}

    Returns:
        result (json): Data
    """

    # TODO: date arg check function?

    conn = utils.conn_to_database()
    result = {}

    # check the args
    args = utils.args_check_date(args, conn)
    sql = utils.generate_sql(args, date_type="range", required_one_of=[])

    df = pd.read_sql(sql, conn)

    # rename columns using formatted model names
    args['model'] = []
    for model in list(set(utils.models_desc.keys()) & set(df.columns)):
        model_name = utils.models_desc[model]['name']
        df.rename(columns={model: model_name}, inplace=True)
        args['model'].append(model_name)

    # add models in the args dict before passing the df to the reformat_json function (which need models in the args)
    # args = utils.args_check_model(args)

    # reformat to json
    result['data'] = utils.reformat_json(df=df, args=args)

    return result

