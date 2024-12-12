from pathlib import Path
import pandas as pd
import requests
import os
import dotenv

from api_client import APIClient

BASE_DIR = Path(__file__).resolve().parent.joinpath('data')
ENV = BASE_DIR.parent.parent.joinpath('.env')
print(ENV)
assert ENV.exists(), f"{ENV} does not exist."
dotenv.load_dotenv(ENV)


def main(delete_national: bool = False, delete_subnational: bool = False):
    post_username = os.getenv("POSTGRES_USER", "")
    post_password = os.getenv("POSTGRES_PASSWORD", "")
    delete_username = os.getenv("POSTGRES_DELETE_USERNAME", "")
    delete_password = os.getenv("POSTGRES_DELETE_PASSWORD", "")
    root_url = "http://3.11.85.207/api/v2"
    post_national_level_dir = BASE_DIR.joinpath("post/national")
    post_subnational_level_dir = BASE_DIR.joinpath("post/subnational")
    delete_national_level_dir = BASE_DIR.joinpath("delete/national")
    delete_subnational_level_dir = BASE_DIR.joinpath("delete/subnational")
    errors_csv_dir = BASE_DIR.joinpath("errors")
    backup_dir = BASE_DIR.joinpath("backup")
    client = APIClient(
        post_username=post_username,
        post_password=post_password,
        delete_username=delete_username,
        delete_password=delete_password,
        root_url=root_url,
        errors_csv_dir=errors_csv_dir,
        backup_dir=backup_dir,
        post_national_level_dir=post_national_level_dir,
        post_subnational_level_dir=post_subnational_level_dir,
        delete_national_level_dir=delete_national_level_dir,
        delete_subnational_level_dir=delete_subnational_level_dir,
    )
    client.post_national_data()
    client.post_subnational_data()
    client.create_backup()
    # These should be put before backup if you want ALL the data backed up 
    # before deleting it.
    if delete_national:
        client.delete_national_data()
    if delete_subnational:
        client.delete_subnational_data()


if __name__ == "__main__":
    main(delete_national=False, delete_subnational=False)
