from app import utils
import pandas as pd
import re

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





def query_specific_country(args):
    conn = utils.conn_to_database()
    result = {}
    if len(args) == 0:
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments.", 400
    elif len(args) == 1:
        sql = utils.generate_sql(args, required_one_of=['iso3code', 'iso2code', 'country'])

        # dates
        data = pd.read_sql(sql, conn)

        data['date'] = data['date'].apply(int)
        data.set_index(keys='date',drop=True,inplace=True)
        result['data'] = data.to_dict()

        for colname in ['country','iso3code','iso2code']:
            result['data'] = utils.rewrite_country_name_dict(result['data'], colname)

        result['status'] = 200
        return result
    else:
        # TODO: do we need to allow multiple country query here?
        return "<h1>400 Error</h1><p>Bad Request: This API endpoint requires arguments."


# data = pd.read_csv('/Users/valler/Python/RA/Gender_Inequality/dgg-www/sql/initial_data/mau_upper_monthly_model_2_2022-06.csv')

# utils.generate_sql(args=)
# args = {"model":'["ground_truth_internet_gg","internet_online_model_prediction"]',"date":'[202207,202206]'}
# args = {"date":'[202207,202206]'，}


def query_national(args):
    # TODO: Better Error handle
    # date must be list or empty
    conn = utils.conn_to_database()
    result = {}
    models = ["ground_truth_internet_gg","internet_online_model_prediction","internet_online_offline_model_prediction","internet_offline_model_prediction","ground_truth_mobile_gg","mobile_online_model_prediction","mobile_online_offline_model_prediction","mobile_offline_model_prediction"]

    # first clean up args -
    if "model" in args.keys():
        args["model"] = re.findall("\"(\w+)\"", args['model'])

    else:
        args["model"] = []

    if "date" in args.keys():
        dates = [int(x) for x in re.findall("(\d{6})", args['date'])]
        args["date"] = args["date"].replace("[","(").replace("]",")")
        # TODO: check the date format
    else:
        sql = "SELECT max(date) FROM  dgg;"
        latest_date = int(pd.read_sql(sql, conn)['max'].values[0])
        args["date"] = f"({latest_date})"
        dates = [latest_date]


    # generate sql
    sql = utils.generate_sql(args, required_one_of=[])
    df = pd.read_sql(sql, conn)

    # convert data into the required format

    # restore date column where there is only one date
    if 'date' not in df.columns:
        df['date'] = [int(re.findall("(\d{6})",args["date"])[0])]*len(df)
    df['date'] = df['date'].apply(int)

    # update the model set
    args['model']= set(models).intersection(df.columns)
    # reformat the data
    data = {}
    for iso2code in df["iso2code"].unique():
        date_dict = {}
        for date in dates:
            model_dict = {}
            for model in args["model"]:
                try:
                    model_dict[model] = df.loc[(df['date']==date) & (df['iso2code']==iso2code)][model].values[0]
                except:
                    model_dict[model] = None
            date_dict[date]=model_dict
        data[iso2code]=date_dict

    result['data'] = data
    result['status'] = 200

    return result


"""
pd.read_sql(sql_query, conn)

conn = create_engine('postgresql+psycopg2://'+
                           "postgres" + ':' +
                           "dgg" + '@' +
                           "localhost"+ ':5432/' +
                           "dggpanel")
"""
