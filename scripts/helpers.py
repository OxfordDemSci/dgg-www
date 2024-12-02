import requests
from enum import Enum
import pandas as pd
from io import BytesIO
from typing import Union

ROOT_URL = "http://localhost:8080/api/v2"


class Level(Enum):
    NATIONAL = "national"
    SUBNATIONAL = "subnational"


def get_token(username: str, password: str):
    data = {
        "username": username,
        "password": password
    }
    url = f"{ROOT_URL}/login"
    response = requests.post(url, json=data)
    return response.json()["access_token"]


def get_date_range(national_or_subnational: Level) -> dict[str, str]:
    init_data = requests.get(f"{ROOT_URL}/init")
    dates = {}
    dates["from"] = init_data.json()[national_or_subnational.value]["dates"][0]
    dates["to"] = init_data.json()[national_or_subnational.value]["dates"][-1]
    return dates


def download_csv(national_or_subnational: Level, date_from: str, date_to: str) -> Union[list[dict], None]:
    url = f"{ROOT_URL}/download_csv?level={national_or_subnational.value}&start_date={date_from}&end_date={date_to}"
    response = requests.get(url)
    if response.status_code == 200:
        csv_bytes = response.content
        df = pd.read_csv(BytesIO(csv_bytes))
        return df.to_dict(orient="records")
    return None

