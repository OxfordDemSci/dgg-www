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
   python post_subnational.py
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
    response.status_code == 200, response.json()


def post_data_from_csv(path_to_csv: Union[Path, str], level: helpers.Level):
    """Posts data from a CSV file."""
    assert Path(path_to_csv).exists(), "CSV File does not exist."
    df = pd.read_csv(path_to_csv)
    chunk_size = 1000
    token = helpers.get_token(username=POST_USERNAME, password=POST_PASSWORD)
    print("POSTING DATA...")
    for start in range(0, len(df), chunk_size):
        end = start + chunk_size
        chunk = df.iloc[start:end]
        data = chunk.to_dict(orient="records")
        post_data(token, data, level)
        print(f"Posted {start} to {end} records.")
    print("POSTED DATA.")


if __name__ == "__main__":
    CSV = BASE.joinpath("test_post_delete_subnational.csv")

    post_data_from_csv(CSV, helpers.Level.SUBNATIONAL)
