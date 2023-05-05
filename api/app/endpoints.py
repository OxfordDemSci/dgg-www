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

        # list countries with national-level data
        sql = 'SELECT iso2,name FROM country_info;'
        data = pd.read_sql(sql, conn)
        result['countries'] = sorted([{'iso2code': x, 'country': y} for x, y in zip(data['iso2'], data['name'])],
                                     key=lambda k: k['iso2code'])

        # list dates with data
        sql = 'SELECT DISTINCT date FROM national;'
        data = pd.read_sql(sql, conn)
        result['dates'] = data['date'].tolist()
        result['dates'] = [int(x) for x in result['dates']]
        result['dates'].sort()

        # list models
        result['models'] = utils.models_desc

        # list model types
        # result['types'] = ['internet', 'mobile']

        # color palette
        result['palette'] = utils.palette(n=6)

        # contact
        result['contact'] = 'ridhi.kashyap@nuffield.ox.ac.uk'

        # http status code and message
        result['status'] = 200
        result['message'] = 'OK: Init endpoint successful.'

    except:

        # http status code and message
        result['status'] = 500
        result['message'] = 'Internal Server Error: Init endpoint failed.'

    return result


def query_specific_country(args):
    """
    API endpoint to query the database for all dates from one country

    Parameters:
        args (dict): A dictionary containing items iso2code (str) and model (list; optional)

    Examples:
        - args = {"iso2code": "AT"}
        - args = {"iso2code": "AT", "model": ["ground_truth_mobile_gg"]}

    Returns:
        result (dict):
    """


    # add model argument if missing
    if 'model' not in args.keys():
        args['model'] = []

    # check and format arguments
    result = utils.check_args(args, required=['iso2code'], optional=['model'])

    # pop formatted arguments from result
    args = result.pop('args')

    if result.get('status') == 200:

        try:

            # connect to database
            conn = utils.conn_to_database()

            # construct sql statement
            sql = "SELECT date, iso2, iso3, name, " + ",".join(args.get("model")) + " " + \
                  "FROM national LEFT JOIN country_info USING (iso2) " + \
                  "WHERE iso2 = '" + args.get('iso2code') + "';"

            # execute sql request and fetch result as data frame
            df = pd.read_sql(sql, conn)

            # reformat data as json
            result['data'] = utils.reformat_json(df)

            # http status message
            result['message'] = "OK: Data successfully selected from database."

        except:

            # http status message and code
            result['status'] = 500
            result['message'] = 'Internal Server Error: Error returned from PostgreSQL server on SELECT.'

    return result


def query_national(args):
    """
    API endpoint to query a single date for all countries

    Parameters:
        args (dict): A dictionary containing items date (int) and model (list)

    Examples:
        - args = {"date": 202207, "model": ["ground_truth_internet_gg"]}
        - args = {"date": 202207}

    Returns:
        result (json): Data
    """

    # add model argument if missing
    if 'model' not in args.keys():
        args['model'] = []

    # check and format arguments
    result = utils.check_args(args, required=['date'], optional=['model'])

    # pop formatted arguments from result
    args = result.pop('args')

    if result['status'] == 200:

        try:

            # connect to database
            conn = utils.conn_to_database()

            # construct sql statement
            sql = "SELECT date, iso2, iso3, name, " + ",".join(args.get("model")) + " " + \
                  "FROM national LEFT JOIN country_info USING (iso2) " + \
                  "WHERE date = " + str(args.get('date')) + ";"

            # execute sql query and fetch result as data frame
            df = pd.read_sql(sql, conn)

            # reformat data to json
            result['data'] = utils.reformat_json(df)

            # http status message
            result['message'] = "OK: Data successfully selected from database."

        except:

            # http status message and code
            result['status'] = 500
            result['message'] = "Internal Server Error: Error returned from PostgreSQL server on SELECT."

    return result


def download_data_with_dates(args):
    """
    Enable the download function to download data between start date and end date

    Parameters:
        args (dict): A dictionary containing items start_date (int) and end_date (int)

    Examples:
        - args = {"start_date":202206, "end_date":202207}

    Returns:
        result (json): Data
    """

    # formatted names
    if 'pretty_names' not in args.keys():
        args['pretty_names'] = True

    # check and format arguments
    result = utils.check_args(args, required=['start_date', 'end_date'], optional=['pretty_names'])

    # pop arguments from result
    args = result.pop('args')

    if result['status'] == 200:

        try:

            # connect to database
            conn = utils.conn_to_database()

            if args.get('pretty_names'):
                # sql sub-statement to query columns and rename them in result
                col_names = [key + ' AS "' + utils.models_desc[key]['name'] + '"' for key in utils.models_desc.keys()]
            else:
                # use un-formatted column names
                col_names = list(utils.models_desc.keys())

            # construct sql statement
            sql = "SELECT date, iso2, iso3, name, " + ",".join(col_names) + " " + \
                  "FROM national LEFT JOIN country_info USING (iso2) " + \
                  "WHERE date >= " + str(args.get('start_date')) + " AND " + \
                  "date <= " + str(args.get('end_date')) + ";"

            # execute sql request and fetch result as data frame
            df = pd.read_sql(sql, conn)

            # reformat to json
            result['data'] = utils.reformat_json(df)

            # http status message
            result['message'] = 'OK: Data successfully selected from database.'

        except:

            # http status message and code
            result['status'] = 500
            result['message'] = "Internal Server Error: Error returned from PostgreSQL server on SELECT."

    return result


def write_national(args):
    """
    API endpoint to write new data into DGG website database.

    Args:
        args (dict): Names and values to be written into database.

    Examples:
         - args = {'date': 202210, 'iso2': 'AT', 'Ground_Truth_Internet_GG': 0.5, 'token':'2tBGBpMeh'}

    Returns:
        dict: http status code (status) and error message (message).

    """
    # check arguments
    result = utils.check_args(args,
                              required=['date', 'iso2', 'token'],
                              optional=["internet_online_model_prediction",
                                        "internet_online_offline_model_prediction",
                                        "internet_offline_model_prediction",
                                        "ground_truth_internet_gg",
                                        "mobile_online_model_prediction",
                                        "mobile_online_offline_model_prediction",
                                        "mobile_offline_model_prediction",
                                        "ground_truth_mobile_gg"])

    # pop reformatted arguments from result
    args = result.pop('args')
    if result['status'] == 200:

        try:
            # connect to database
            conn = utils.conn_to_database(mode='w')

            # add single quotes around string values to meet PostgreSQL format
            for key in args.keys():
                if isinstance(args.get(key), str):
                    args[key] = f"'{args.get(key)}'"

            # construct SQL statement
            cols = ','.join(args.keys())
            vals = ','.join([str(i) for i in args.values()])
            sql = f"INSERT INTO national({cols}) VALUES({vals});"

            # execute SQL request
            conn.execute(sql)

            # http status message
            result['message'] = 'OK: Data successfully written to database.'

        except:

            # http status message and code
            result['status'] = 500
            result['message'] = "Internal Server Error: Error returned from PostgreSQL server on INSERT."

    return result
