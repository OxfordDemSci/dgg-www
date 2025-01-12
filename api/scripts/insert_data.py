import os
from pathlib import Path
import sys
import pycountry
import numpy as np

from alembic import command
from alembic.config import Config

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
import fiona
import geopandas as gpd
from geoalchemy2 import shape
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from shapely import wkt
from shapely.geometry import shape
from dotenv import load_dotenv

from app.models import (
    SubNationalIndicators,
    NationalIndicators,
    SubNationalGeometries,
    NationalGeomeries,
    NationalGroundTruth,
    SubNationalGroundTruth,
    SubNationalNames,
    DGGIndicatorDescription
)

BASE = Path(__file__).resolve().parent.joinpath("data")
assert BASE.exists(), f"Path {BASE} does not exist."
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
if os.getenv("ENV") == "dev":
    DATABASE_URL = os.getenv("DATABASE_URL", "")
else:
    DATABASE_URL = os.getenv("DATABASE_URL_LOCAL", "")
POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DB = os.getenv("POSTGRES_DB", "")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def upgrade_alembic():
    if os.getenv("ENV") != "local":
        pg_host = "dgg_db"
    else:
        pg_host = "localhost"
    alembic_cfg = Config(BASE_DIR.joinpath("alembic.ini"))
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{pg_host}:5432/{POSTGRES_DB}",
    )
    command.upgrade(alembic_cfg, "head")


def delete_all_rows(table_name):
    # Check if the table exists
    table_exists_query = text(f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = :table_name
        )
    """)
    result = session.execute(table_exists_query, {'table_name': table_name}).scalar()
    
    if result:
        # If the table exists, truncate it
        session.execute(text(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE'))
        session.commit()
    else:
        print(f"Table {table_name} does not exist.")


def get_country_name(row):
    try:
        country = pycountry.countries.get(alpha_3=row['gid_0'])
        return country.name
    except AttributeError:
        return row['gid_0']


def upload_csv_to_indicators(csv_path, table_model):
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m").dt.strftime('%Y-%m')
    df['country'] = df.apply(get_country_name, axis=1)
    df = df.replace({np.nan: None, 'NaN': None, 'nan': None, 'null': None, 'NULL': None, 'None': None})
    data = df.to_dict(orient='records')
    session.bulk_insert_mappings(table_model, data)
    session.commit()


def upload_ground_truth_data(csv_path, table_model):
    df = pd.read_csv(csv_path)
    df = df.replace({np.nan: None, 'NaN': None, 'nan': None, 'null': None, 'NULL': None, 'None': None})
    data = df.to_dict(orient='records')
    session.bulk_insert_mappings(table_model, data)
    session.commit()


def upload_geopackage_to_subnational_geometries(geopackage_path, layer_name):
    with fiona.open(geopackage_path, layer=layer_name) as src:
        for feature in src:
            if layer_name == "L0":
                geom = shape(feature['geometry']).wkt
                data = {
                    "fid": feature['id'],
                    "gid_0": feature['properties']['GID_0'],
                    "geom": geom
                }
                session.add(NationalGeomeries(**data))
            elif layer_name == "L1":
                geom = shape(feature['geometry']).wkt
                data = {
                    "fid": feature['id'],
                    "gid_0": feature['properties']['GID_0'],
                    "gid_1": feature['properties']['GID_1'],
                    "name_1": feature['properties']['NAME_1'],
                    "is_subnational": feature['properties']['is_subnational'],
                    "geom": geom
                }
                session.add(SubNationalGeometries(**data))
    session.commit()


def main():
    upgrade_alembic()
    tables = ["subnational_geometries", "national_geometries", "subnational_indicators", "national_indicators"] #, "indicator_descriptions"]
    for table in tables:
        delete_all_rows(table)
    csv_path_subnational = BASE / "subnational_estimates_2024-05-01_2024-07_01.csv"
    csv_path_national = BASE / "national_estimates_2024-05-01_2024-07_01.csv"
    ground_truth_national_csv_path = BASE / "national_ground_truth.csv"
    national_ground_truth_model = NationalGroundTruth
    ground_truth_subnational_csv_path = BASE / "subnational_ground_truth.csv"
    subnational_ground_truth_model = SubNationalGroundTruth
    subnational_names_csv_path = BASE / "adm_1_names.csv"
    subnational_names_model = SubNationalNames
    indicator_descriptions_csv_path = BASE / "indicator_descriptions.csv"
    indicator_descriptions_model = DGGIndicatorDescription
    geopackage_path = BASE / "simplified_l0_l1.gpkg"
    layers = ["L0", "L1"]
    upload_csv_to_indicators(csv_path_subnational, SubNationalIndicators)
    upload_csv_to_indicators(csv_path_national, NationalIndicators)
    upload_ground_truth_data(ground_truth_national_csv_path, national_ground_truth_model)
    upload_ground_truth_data(ground_truth_subnational_csv_path, subnational_ground_truth_model)
    upload_ground_truth_data(subnational_names_csv_path, subnational_names_model)
    upload_ground_truth_data(indicator_descriptions_csv_path, indicator_descriptions_model)
    # for layer_name in layers:
    #     upload_geopackage_to_subnational_geometries(geopackage_path, layer_name)
    session.close()


if __name__ == "__main__":
    main()
