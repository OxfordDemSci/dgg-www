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

    result = {'status': 200, 'message': 'OK: Successfully initialized.'}

    try:
        conn = utils.conn_to_database()

        # list model types
        result['types'] = ['internet', 'mobile']

        # list models
        result['models'] = utils.models_desc

        # list countries with national-level data
        sql = 'SELECT iso2,name FROM country_info;'
        data = pd.read_sql(sql, conn)
        result['countries'] = [{'iso2code': x, 'country': y} for x, y in zip(data['iso2'], data['name'])]

        # list dates with data
        sql = 'SELECT DISTINCT date FROM national;'
        data = pd.read_sql(sql, conn)
        result['dates'] = data['date'].tolist()
        result['dates'] = [int(x) for x in result['dates']]

        # color palette
        result['palette'] = utils.palette(n=6)

        # contact
        result['contact'] = 'digitalgendergaps@gmail.com'

    except:
        result['status'] = 500
        result['message'] = 'Internal Server Error: Init endpoint failed.'

    return result


def query_specific_country(args):
    """
    API endpoint to query the database for one country at one time

    Parameters:
        args (dict): A dictionary containing items iso2code (str) and model (list; optional)

    Examples:
        - args = {"iso2code": "AT"}
        - args = {"iso2code": "AT", "model": ["ground_truth_mobile_gg"]}

    Returns:
        result (dict):
    """

    if 'model' not in args.keys():
        args['model'] = []

    result = utils.check_args(args, required=['iso2code'], optional=['model'])
    args = result.pop('args')

    if result.get('status') == 200:

        try:
            conn = utils.conn_to_database()

            sql = "SELECT date, iso2, iso3, name, " + ",".join(args.get("model")) + " " + \
                  "FROM national LEFT JOIN country_info USING (iso2) " + \
                  "WHERE iso2 = '" + args.get('iso2code') + "';"
            df = pd.read_sql(sql, conn)

            result['data'] = utils.reformat_json(df)
            result['message'] = "OK: Data successfully selected from database."

        except:
            result['status'] = 500
            result['message'] = 'Internal Server Error: Error returned from PostgreSQL server on SELECT.'

    return result


def query_national(args):
    """
    API endpoint to query the database for all countries

    Parameters:
        args (dict): A dictionary containing items date (int) and model (list)

    Examples:
        - args = {"date": 202207, "model": ["ground_truth_internet_gg"]}
        - args = {"date": 202207}

    Returns:
        result (json): Data
    """

    if 'model' not in args.keys():
        args['model'] = []

    result = utils.check_args(args, required=['date'], optional=['model'])
    args = result.pop('args')

    if result['status'] == 200:

        try:
            conn = utils.conn_to_database()

            sql = "SELECT date, iso2, iso3, name, " + ",".join(args.get("model")) + " " + \
                  "FROM national LEFT JOIN country_info USING (iso2) " + \
                  "WHERE date = " + str(args.get('date')) + ";"

            df = pd.read_sql(sql, conn)

            result['data'] = utils.reformat_json(df)
            result['message'] = "OK: Data successfully selected from database."

        except:
            result['status'] = 500
            result['message'] = "Internal Server Error: Error returned from PostgreSQL server on SELECT."

    return result


def download_data_with_dates(args={}):
    """
    Enable the download function to download data by 2 dates (start dates and end dates)

    Parameters:
        args (dict): A dictionary containing items start_date (int) and end_date (int)

    Examples:
        - args = {"start_date":202206, "end_date":202207}

    Returns:
        result (json): Data
    """

    result = utils.check_args(args, required=['start_date', 'end_date'])
    args = result.pop('args')

    if result['status'] == 200:

        try:
            conn = utils.conn_to_database()

            col_names = [key + ' AS "' + utils.models_desc[key]['name'] + '"' for key in utils.models_desc.keys()]

            sql = "SELECT date, iso2, iso3, name, " + ",".join(col_names) + " " + \
                  "FROM national LEFT JOIN country_info USING (iso2) " + \
                  "WHERE date >= " + str(args.get('start_date')) + " AND " + \
                  "date <= " + str(args.get('end_date')) + ";"

            df = pd.read_sql(sql, conn)

            # reformat to json
            result['data'] = utils.reformat_json(df)
            result['message'] = 'OK: Data successfully selected from database.'

        except:
            result['status'] = 500
            result['message'] = "Internal Server Error: Error returned from PostgreSQL server on SELECT."

    return result


def write_national(args):
    """
    API endpoint to write new data into DGG website database.

    Args:
        args (dict): Names and values to be written into database.

    Examples:
         - args = {'date': 202210, 'iso2': "'AT'", 'Ground_Truth_Internet_GG': 0.5}

    Returns:
        dict: http status code (status) and error message (message).

    """
    result = utils.check_args(args,
                              required=['date', 'iso2'],
                              optional=['Ground_Truth_Internet_GG',
                                        'Internet_Online_model_prediction',
                                        'Internet_Online_Offline_model_prediction',
                                        'Internet_Offline_model_prediction',
                                        'Ground_Truth_Mobile_GG',
                                        'Mobile_Online_model_prediction',
                                        'Mobile_Online_Offline_model_prediction',
                                        'Mobile_Offline_model_prediction'])
    args = result.pop('args')

    if result['status'] == 200:

        try:
            conn = utils.conn_to_database(mode='w')

            sql = "INSERT INTO national({}) VALUES({});".format(','.join(args.keys()), ','.join([str(i) for i in args.values()]))

            conn.execute(sql)

            result['message'] = 'OK: Data successfully written to database.'

        except:
            result['status'] = 500
            result['message'] = "Internal Server Error: Error returned from PostgreSQL server on INSERT."

    return result
