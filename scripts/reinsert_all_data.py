import os
from pathlib import Path
import sys
import pycountry
import numpy as np
from contextlib import contextmanager
from memory_profiler import profile

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

engine = create_engine(DATABASE_URL, pool_size=50, max_overflow=10)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


def delete_all_rows(table_name):
    session = Session()
    try:
        session.execute(text(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE'))
        session.commit()
    except Exception as e:
        print(f"Error deleting rows from {table_name}: {e}")
        session.rollback()
    finally:
        session.close()


def get_country_name(row):
    try:
        country = pycountry.countries.get(alpha_3=row['gid_0'])
        return country.name
    except AttributeError:
        return row['gid_0']


@profile
def upload_csv_to_indicators(csv_path, table_model, session, chunk_size=1000):
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m").dt.strftime('%Y-%m')
    df['country'] = df.apply(get_country_name, axis=1)
    df = df.replace({np.nan: None, 'NaN': None, 'nan': None, 'null': None, 'NULL': None, 'None': None})
    for i in range(0, len(df), chunk_size):
        data_chunk = df.iloc[i:i+chunk_size].to_dict(orient='records')
        session.bulk_insert_mappings(table_model, data_chunk)
        session.commit()


def main():
    tables = {"subnational": "subnational_indicators", "national": "national_indicators"}
    for level, table in tables.items():
        try:
            csv = next(x for x in BASE.joinpath(level).iterdir() if x.suffix == ".csv")
            with session_scope() as session:
                delete_all_rows(table)
                model = SubNationalIndicators if level == "subnational" else NationalIndicators
                upload_csv_to_indicators(csv, model, session)
                print(f"Uploaded {level} data to {table} table.")
        except StopIteration:
            print(f"No csv found for {level} data.")
        except Exception as e:
            print(f"Error uploading {level} data: {e}")


if __name__ == "__main__":
    main()
