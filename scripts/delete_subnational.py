"""
    This script has functions to delete data from the database. After logging in and getting a token, the options are:
    - delete_data: Delete data using a list of dictionaries representing the data to be deleted.
    - delete_data_from_csv: Delete data using a CSV file representing the data to be deleted. If there is a 
    requirement to empty the database, one could run the download csv endpoint in the range of ALL dates, and 
    then use this csv to empty the database.
"""
import requests
from pathlib import Path
import pandas as pd
import os
import dotenv
from typing import Union

import helpers

BASE = Path(__file__).resolve().parent
ROOT_URL = "http://3.11.85.207/api/v2"

ENV_FILE = BASE.parent / ".env"  # Path to .env file with credentials

dotenv.load_dotenv(ENV_FILE)  # Load credentials from .env file

DELETE_USERNAME = os.getenv("POSTGRES_DELETE_USERNAME")
DELETE_PASSWORD = os.getenv("POSTGRES_DELETE_PASSWORD")


def delete_data(token: str, data: list[dict], level: helpers.Level):
    """Delete data using a list of dictionaries representing the data to be deleted."""
    url = f"{ROOT_URL}/delete_{level.value}_data"
    response = requests.delete(url, json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.json()
    return response.json()


def delete_data_from_csv(path_to_csv: Union[Path, str]):
    """Deletes data from a CSV file."""
    assert Path(path_to_csv).exists(), "CSV File does not exist."
    df = pd.read_csv(path_to_csv)
    data = df.to_dict(orient="records")
    token = helpers.get_token(username=DELETE_USERNAME, password=DELETE_PASSWORD)
    response = delete_data(token, data, helpers.Level.SUBNATIONAL)
    print(response)


if __name__ == "__main__":
    CSV = BASE.joinpath(("test_post_delete_subnational.csv"))
    delete_data_from_csv(CSV)