from pathlib import Path
import pandas as pd
import pycountry


from app.models import (
    SubNationalIndicators,
    NationalIndicators,
    NationalGroundTruth,
    SubNationalGroundTruth,
    SubNationalNames,
    DGGIndicatorDescription
)

TEST_DATA = Path(__file__).resolve().parent.joinpath("test_data")
ADM_NAMES = TEST_DATA.joinpath("adm1_names_test.csv")
NATIONAL_INDICATORS = TEST_DATA.joinpath("national_indicators_test.csv")
SUBNATIONAL_INDICATORS = TEST_DATA.joinpath("subnational_indicators_test.csv")
NATIONAL_GROUND_TRUTH = TEST_DATA.joinpath("national_ground_truth_test.csv")
SUBNATIONAL_GROUND_TRUTH = TEST_DATA.joinpath("subnational_ground_truth_test.csv")
INDICATOR_DESCRIPTIONS = TEST_DATA.joinpath("indicator_descriptions.csv")


def insert_test_data(session):
    upload_csv_to_indicators(SUBNATIONAL_INDICATORS, SubNationalIndicators, session)
    upload_csv_to_indicators(NATIONAL_INDICATORS, NationalIndicators, session)
    upload_ground_truth_data(NATIONAL_GROUND_TRUTH, NationalGroundTruth, session)
    upload_ground_truth_data(SUBNATIONAL_GROUND_TRUTH, SubNationalGroundTruth, session)
    upload_ground_truth_data(ADM_NAMES, SubNationalNames, session)
    upload_ground_truth_data(INDICATOR_DESCRIPTIONS, DGGIndicatorDescription, session)


def upload_csv_to_indicators(csv_path, table_model, session):
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m").dt.strftime('%Y-%m')
    df['country'] = df.apply(get_country_name, axis=1)
    data = df.to_dict(orient='records')
    session.bulk_insert_mappings(table_model, data)
    session.commit()


def upload_ground_truth_data(csv_path, table_model, session):
    df = pd.read_csv(csv_path)
    data = df.to_dict(orient='records')
    session.bulk_insert_mappings(table_model, data)
    session.commit()


def get_country_name(row):
    try:
        country = pycountry.countries.get(alpha_3=row['gid_0'])
        return country.name
    except AttributeError:
        return row['gid_0']