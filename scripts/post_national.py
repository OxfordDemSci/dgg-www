"""
This script is designed to post subnational data to the API. It reads data from a CSV file,
converts it into a list of dictionaries, and then posts this data to the API using an authorisation token.

How to run the script:
1. Ensure you have a .env file in the parent directory with the necessary environment variables, including:
   - POSTGRES_USER
   - POSTGRES_PASSWORD
2. Place the CSV file containing the data to be posted in the appropriate directory.
3. Run the script using Python:
   ```
   python post_national.py
   ```
"""

import pandas as pd
import requests
from enum import Enum
import os
from pathlib import Path
import dotenv
import helpers
from typing import Union
import pycountry

BASE = Path(__file__).resolve().parent

ROOT_URL = "http://3.11.85.207/api/v2"

ENV_FILE = BASE.parent / ".env"

dotenv.load_dotenv(ENV_FILE)

POST_USERNAME = os.getenv("POSTGRES_USER", "")
POST_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")


def post_data(token: str, data: list[dict], level: helpers.Level):
    """Post data using a list of dictionaries representing the data to be posted."""
    url = f"{ROOT_URL}/post_{level.value}_data"
    response = requests.post(url, json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.json()


def post_data_from_csv(path_to_csv_dir: Union[Path, str], level: helpers.Level):
    """Posts data from a CSV file."""
    assert Path(path_to_csv_dir).exists(), "CSV File does not exist."
    csv_files = list(Path(path_to_csv_dir).rglob("*.csv"))
    for path_to_csv in csv_files:
        df = pd.read_csv(path_to_csv)
        if "country" not in df.columns:
            df["country"] = df.apply(lambda x: pycountry.countries.get(alpha_3=x["gid_0"]).name, axis=1)
        chunk_size = 1000
        token = helpers.get_token(username=POST_USERNAME, password=POST_PASSWORD)
        print("POSTING DATA...")
        for start in range(0, len(df), chunk_size):
            end = start + chunk_size
            chunk = df.iloc[start:end]
            data = chunk.to_dict(orient="records")
            post_data(token, data, level)
            print(f"Posted {start} to {end} records.")
        print(f"POSTED DATA FROM {path_to_csv.name}.")
    print("POSTED DATA.")


if __name__ == "__main__":
    #CSV = BASE.joinpath("test_post_delete_national.csv")
    #CSV_DIR = BASE.joinpath("dgg_data_national/dgg_data_national")
    CSV_DIR = BASE.joinpath("dgg_test_upload")
    from datetime import datetime
    start = datetime.now()
    post_data_from_csv(CSV_DIR, helpers.Level.NATIONAL)
    end = datetime.now()
    print(f"Time taken to post data: {end-start}")
