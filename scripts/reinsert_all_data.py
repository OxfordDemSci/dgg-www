import os
from pathlib import Path
import sys
import pycountry

sys.path.append(str(Path(__file__).resolve().parent.parent / "api"))

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.models import (
    SubNationalIndicators,
    NationalIndicators,
)

BASE = Path(__file__).resolve().parent.joinpath("data/post")
assert BASE.exists(), f"Path {BASE} does not exist."
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL_LOCAL", "")
POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DB = os.getenv("POSTGRES_DB", "")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

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
    data = df.to_dict(orient='records')
    session.bulk_insert_mappings(table_model, data)
    session.commit()


def upload_ground_truth_data(csv_path, table_model):
    df = pd.read_csv(csv_path)
    data = df.to_dict(orient='records')
    session.bulk_insert_mappings(table_model, data)
    session.commit()


def main():
    tables = {"subnational": "subnational_indicators", "national": "national_indicators"}
    for level, table in tables.items():
        try:
            csv = next(x for x in BASE.joinpath(level).iterdir() if x.suffix == ".csv")
            delete_all_rows(table)
            model = SubNationalIndicators if level == "subnational" else NationalIndicators
            upload_csv_to_indicators(csv, model)
            print(f"Uploaded {level} data to {table} table.")
        except StopIteration:
            print(f"No csv found for {level} data.")
    session.close()


if __name__ == "__main__":
    main()
