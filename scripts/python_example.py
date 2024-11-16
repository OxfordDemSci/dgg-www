"""
Python script to interact with the API

Credentials are in the .env file at the root of the project server. Please contact GISRede if you need these separately.

You will need POSTGRES_USER and POSTGRES_PASSWORD to post data
You will need POSTGRES_DELETE_USERNAME and POSTGRES_DELETE_PASSWORD to delete data
"""

import requests
import dotenv
from pathlib import Path
import os
import pandas as pd

BASE = Path(__file__).resolve().parent
ENV_FILE = BASE.parent / ".env"

ROOT_URL = "http://3.11.85.207/api/v2"

dotenv.load_dotenv()


def get_token(username: str, password: str):
    data = {
        "username": username,
        "password": password
    }
    url = f"{ROOT_URL}/login"
    response = requests.post(url, json=data)
    return response.json()["access_token"]


def get_data():
    url = f"{ROOT_URL}/get_subnational_data?date=2024-05&country=AFG"
    response = requests.get(url)
    return response.json()


def get_csv_data():
    post_csv = BASE / "test_post_delete.csv"
    df = pd.read_csv(post_csv)
    data = df.to_dict(orient="records")  # Convert dataframe to list of dictionaries
    return data


def post_data(token: str):
    data = get_csv_data()
    url = f"{ROOT_URL}/post_subnational_data"
    #  for row in data:
    response = requests.post(url, json=data, headers={"Authorization": f"Bearer {token}"})
    return response.json()


def delete_data(token: str):
    data = get_csv_data()
    url = f"{ROOT_URL}/delete_subnational_data"
    response = requests.delete(url, json=data, headers={"Authorization": f"Bearer {token}"})
    return response.json()


def main():
    username = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    token = get_token(username, password)

    #  GET DATA
    data = get_data()
    print(data)

    #  POST DATA
    #  This can contain an error if the data already exists
    post_response = post_data(token)
    print(post_response)

    #  DELETE DATA
    #  You need to sign in with the the DELETE USERNAME
    #  This can contain an error if the data does not exist
    delete_username = os.getenv("POSTGRES_DELETE_USERNAME")
    delete_password = os.getenv("POSTGRES_DELETE_PASSWORD")
    delete_token = get_token(delete_username, delete_password)
    delete_response = delete_data(delete_token)
    print(delete_response)


if __name__ == "__main__":
    main()
