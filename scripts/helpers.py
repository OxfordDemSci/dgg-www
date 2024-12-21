import requests
from enum import Enum
import pandas as pd
from io import BytesIO
from typing import Union
import json


class Level(Enum):
    NATIONAL = "national"
    SUBNATIONAL = "subnational"


def get_token(root_url: str, username: str, password: str):
    data = {
        "username": username,
        "password": password
    }
    url = f"{root_url}/login"
    response = requests.post(url, json=data)
    return response.json()["access_token"]


def get_date_range(root_url: str, national_or_subnational: Level) -> Union[dict[str, str] | None]:
    init_data = requests.get(f"{root_url}/init")
    dates = {}
    if init_data.json()[national_or_subnational.value]["dates"]:
        dates["from"] = init_data.json()[national_or_subnational.value]["dates"][0]
        dates["to"] = init_data.json()[national_or_subnational.value]["dates"][-1]
        return dates


def download_csv(root_url: str, national_or_subnational: Level, date_from: str, date_to: str) -> Union[list[dict], None]:
    url = f"{root_url}/download_csv?level={national_or_subnational.value}&start_date={date_from}&end_date={date_to}"
    response = requests.get(url)
    if response.status_code == 200:
        csv_bytes = response.content
        df = pd.read_csv(BytesIO(csv_bytes))
        return df
    return None


def convert_to_df(data: dict) -> pd.DataFrame:
    import re
    if "error" not in data:
        raise Exception(f"Something went wrong - {data}")
    error_data_str = data['error'].split(": ", 1)[1]
    error_data_str = re.sub(r'(?<!\\)\'', '"', error_data_str)
    error_data_str = re.sub(r'(?<=[a-zA-Z])"(?=[a-zA-Z])', "'", error_data_str)
    try:
        error_data_list = json.loads(error_data_str)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print(f"Error at line {e.lineno}, column {e.colno}, char {e.pos}")
        
        # Extract the part of the JSON string around the error location
        error_start = max(e.pos - 50, 0)
        error_end = min(e.pos + 50, len(error_data_str))
        print(f"Problematic part of the JSON string: {error_data_str[error_start:error_end]}")
        
        # Handle the error or raise an exception
        raise
    df = pd.DataFrame(error_data_list)
    return df


