from pathlib import Path
import pandas as pd
import requests
import os
from typing import Union
import pycountry
from datetime import datetime

import helpers


class APIClient:
    def __init__(
            self,
            post_username: str,
            post_password: str,
            delete_username: str,
            delete_password: str,
            root_url: str,
            errors_csv_dir: Union[str | Path],
            backup_dir: Union[str | Path],
            post_national_level_dir: Union[str | Path | None] = None,
            post_subnational_level_dir: Union[str | Path | None] = None,
            delete_national_level_dir: Union[str | Path | None] = None,
            delete_subnational_level_dir: Union[str | Path | None] = None
    ) -> None:
        self.post_username = post_username
        self.post_password = post_password
        self.delete_username = delete_username
        self.delete_password = delete_password
        self.root_url = root_url
        self.post_national_level_dir = Path(post_national_level_dir)
        self.post_subnational_level_dir = Path(post_subnational_level_dir)
        self.delete_national_level_dir = Path(delete_national_level_dir)
        self.delete_subnational_level_dir = Path(delete_subnational_level_dir)
        self.errors_csv_dir = Path(errors_csv_dir)
        self.backup_dir = Path(backup_dir)
        self.post_token = self.get_token(self.post_username, self.post_password)
        self.delete_token = self.get_token(self.delete_username, self.delete_password)
        self.todays_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def get_token(self, username: str, password: str) -> str:
        data = {
            "username": username,
            "password": password
        }
        url = f"{self.root_url}/login"
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise Exception(f"Error getting token for {username}: {response.json()}")
        return response.json()["access_token"]

    def post_national_data(self) -> None:
        assert Path(self.post_national_level_dir).exists(), "CSV DIR does not exist."
        csv_files = list(Path(self.post_national_level_dir).rglob("*.csv"))
        if not csv_files:
            print("No CSV files found in post national directory.")
            return
        df_list = []
        for path_to_csv in csv_files:
            df = pd.read_csv(path_to_csv)
            if "country" not in df.columns:
                df["country"] = df.apply(lambda x: pycountry.countries.get(alpha_3=x["gid_0"]).name, axis=1)
            chunk_size = 1000
            for start in range(0, len(df), chunk_size):
                end = start + chunk_size
                chunk = df.iloc[start:end]
                data = chunk.to_dict(orient="records")
                errors = self._post_data(self.post_token, data, helpers.Level.NATIONAL)
                if errors:
                    try:
                        df_list.append(helpers.convert_to_df(errors))
                    except Exception as e:
                        print(f"Error converting errors to DataFrame: {e}")
                print(f"Posted {start} to {end} records.")
        if df_list:
            errors_df = pd.concat(df_list)
            if not self.errors_csv_dir.exists():
                self.errors_csv_dir.mkdir(parents=True)
            errors_df.to_csv(self.errors_csv_dir.joinpath(f"post_national_errors_{self.todays_date}.csv"), index=False)
            print(f"Post National Errors saved to CSV in {self.errors_csv_dir}. These errors could be the result of duplication of other errors")

    def post_subnational_data(self) -> None:
        assert Path(self.post_subnational_level_dir).exists(), "CSV DIR does not exist."
        csv_files = list(Path(self.post_subnational_level_dir).rglob("*.csv"))
        if not csv_files:
            print("No CSV files found in post subnational directory.")
            return
        df_list = []
        for path_to_csv in csv_files:
            df = pd.read_csv(path_to_csv)
            if "country" not in df.columns:
                df["country"] = df.apply(lambda x: pycountry.countries.get(alpha_3=x["gid_0"]).name, axis=1)
            chunk_size = 1000
            for start in range(0, len(df), chunk_size):
                end = start + chunk_size
                chunk = df.iloc[start:end]
                data = chunk.to_dict(orient="records")
                errors = self._post_data(self.post_token, data, helpers.Level.SUBNATIONAL)
                if errors:
                    df_list.append(helpers.convert_to_df(errors))
                print(f"Posted {start} to {end} records.")
        if df_list:
            errors_df = pd.concat(df_list)
            errors_df.to_csv(self.errors_csv_dir.joinpath(f"post_subnational_errors_{self.todays_date}.csv"), index=False)
            print(f"Post Subnational Errors saved to CSV in {self.errors_csv_dir}. These errors could be the result of duplication of other errors")

    def _post_data(self, token: str, data: list[dict], level: helpers.Level) -> None:
        """Post data using a list of dictionaries representing the data to be posted."""
        url = f"{self.root_url}/post_{level.value}_data"
        response = requests.post(url, json=data, headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            import json
            try:
                return response.json()
            except json.JSONDecodeError:
                # Return None or an error message if JSON parsing fails
                return {"response_error": "Invalid JSON response", "status_code": response.status_code, "body": response.text}
        
    def delete_national_data(self) -> None:
        assert Path(self.delete_national_level_dir).exists(), "CSV File does not exist."
        csv_files = list(Path(self.delete_national_level_dir).rglob("*.csv"))
        if not csv_files:
            print("No CSV files found in delete national directory.")
            return
        df_list = []
        for path_to_csv in csv_files:
            df = pd.read_csv(path_to_csv)
            if "country" not in df.columns:
                df["country"] = df.apply(lambda x: pycountry.countries.get(alpha_3=x["gid_0"]).name, axis=1)
            chunk_size = 1000
            for start in range(0, len(df), chunk_size):
                end = start + chunk_size
                chunk = df.iloc[start:end]
                data = chunk.to_dict(orient="records")
                errors = self._delete_data(self.delete_token, data, helpers.Level.NATIONAL)
                if errors:
                    df_list.append(helpers.convert_to_df(errors))
        if df_list:
            errors_df = pd.concat(df_list)
            errors_df.to_csv(self.errors_csv_dir.joinpath(f"delete_national_errors_{self.todays_date}.csv"), index=False)
            print(f"Delete National Errors saved to CSV in {self.errors_csv_dir}. These errors could be the result of duplication of other errors")
        
    def delete_subnational_data(self) -> None:
        assert Path(self.delete_subnational_level_dir).exists(), "CSV File does not exist."
        csv_files = list(Path(self.delete_subnational_level_dir).rglob("*.csv"))
        if not csv_files:
            print("No CSV files found in delete subnational directory.")
            return
        df_list = []
        for path_to_csv in csv_files:
            df = pd.read_csv(path_to_csv)
            if "country" not in df.columns:
                df["country"] = df.apply(lambda x: pycountry.countries.get(alpha_3=x["gid_0"]).name, axis=1)
            chunk_size = 1000
            for start in range(0, len(df), chunk_size):
                end = start + chunk_size
                chunk = df.iloc[start:end]
                data = chunk.to_dict(orient="records")
                errors = self._delete_data(self.delete_token, data, helpers.Level.SUBNATIONAL)
                if errors:
                    df_list.append(helpers.convert_to_df(errors))
        if df_list:
            errors_df = pd.concat(df_list)
            errors_df.to_csv(self.errors_csv_dir.joinpath(f"delete_subnational_errors_{self.todays_date}.csv"), index=False)
            print(f"Delete Subnational Errors saved to CSV in {self.errors_csv_dir}. These errors could be the result of duplication of other errors")

    def _delete_data(self, token: str, data: list[dict], level: helpers.Level) -> None:
        """Delete data using a list of dictionaries representing the data to be deleted."""
        url = f"{self.root_url}/delete_{level.value}_data"
        response = requests.delete(url, json=data, headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            import json
            try:
                return response.json()
            except json.JSONDecodeError:
                # Return None or an error message if JSON parsing fails
                return {"response_error": "Invalid JSON response", "status_code": response.status_code, "body": response.text}

    def create_backup(self) -> None:
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)
        subnational_date_range = helpers.get_date_range(self.root_url, helpers.Level.SUBNATIONAL)
        national_date_range = helpers.get_date_range(self.root_url, helpers.Level.NATIONAL)
        national_data = None
        subnational_data = None
        if national_date_range is not None:
            national_data = helpers.download_csv(self.root_url, helpers.Level.NATIONAL, national_date_range["from"], national_date_range["to"])
        if subnational_date_range is not None:
            subnational_data = helpers.download_csv(self.root_url, helpers.Level.SUBNATIONAL, subnational_date_range["from"], subnational_date_range["to"])
        if national_data is not None and not national_data.empty:
            national_data.to_csv(self.backup_dir.joinpath(f"national_backup_{self.todays_date}.csv"), index=False)
        else:
            print("No national data to backup. This could be because the table is too large. Please download manually from the API UI")
        if subnational_data is not None and not subnational_data.empty:
            subnational_data.to_csv(self.backup_dir.joinpath(f"subnational_backup_{self.todays_date}.csv"), index=False)
        else:
            print("No subnational data to backup. This could be because the table is too large. Please download manually from the API UI")
