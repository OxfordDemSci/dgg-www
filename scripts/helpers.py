import requests
from enum import Enum
import pandas as pd
from io import BytesIO
from typing import Union
import json

#ROOT_URL = "http://3.11.85.207/api/v2"
#ROOT_URL = "http://localhost:8080/api/v2"


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


def get_date_range(root_url: str, national_or_subnational: Level) -> dict[str, str]:
    init_data = requests.get(f"{root_url}/init")
    dates = {}
    dates["from"] = init_data.json()[national_or_subnational.value]["dates"][0]
    dates["to"] = init_data.json()[national_or_subnational.value]["dates"][-1]
    return dates


def download_csv(root_url: str, national_or_subnational: Level, date_from: str, date_to: str) -> Union[list[dict], None]:
    url = f"{root_url}/download_csv?level={national_or_subnational.value}&start_date={date_from}&end_date={date_to}"
    response = requests.get(url)
    if response.status_code == 200:
        csv_bytes = response.content
        df = pd.read_csv(BytesIO(csv_bytes))
        return df# .to_dict(orient="records")
    return None


def convert_to_df(data: dict) -> pd.DataFrame:
    if "error" not in data:
        raise Exception(f"Something went wrong - {data}")
    error_data_str = data['error'].split(": ", 1)[1]
    error_data_str = error_data_str.replace("'", '"')
    error_data_list = json.loads(error_data_str)
    df = pd.DataFrame(error_data_list)
    return df


