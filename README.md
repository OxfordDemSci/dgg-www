# Digital Gender Gaps V2
The data for this project can be accessed via the dashboard (`http://3.11.85.207/dashboard/`) or the API (`http://3.11.85.207/api/v2/`). The API can be interacted with programatically, or via the Swagger UI (`http://3.11.85.207/api/v2/ui `), which also acts as the API documentation.


## Helper Scripts

**Please see API Client and automation scripts for automating the posting and deleting of data**

There are a couple of the scripts in this repo that demonstrate how to access the data programmatically via the API, and also write and delete data to the database. There is an example script for Python, and the same functionality in R. The scripts can be found int `./scripts/python_example.[py][R]`. The functions demonstrate how to sign in, authenticate with a token, `GET`, `POST` and `DELETE` data.

In order to use the Write and Delete endpoints, the user will need to be authenticated. There are project-wide passwords help in the `.env` file on the server, or contact Daniel Valdenegro if you are unable to `ssh` into the server. The `.env` file is held in the `~/dgg-www` directory.

In order to write to the database, you will need the `POSTGRES_USER` (username) and `POSTGRES_PASSWORD` (password) variables from the `.env` file.

In order to delete from the database, you will need the `POSTGRES_DELETE_USERNAME` (username) and `POSTGRES_DELETE_PASSWORD` (password) variables from the `.env` file.

### Authentication
Authentication to the `POST` and `DELETE` endpoints is a two-step process.
1. `POST` to the `login` endpoint, with your username and password -> This will return your `JWT` token (see `get_token` functions in the example scripts)
2. Make your requests to the `POST` or `DELETE` with your `JWT` token embedded in the request headers (see `post_data` / `delete_data` functions in the example scripts)
**NOTE** The `POST` and `DELETE` endpoints use different credentials to prevent confusion. You will not be able to `POST` using the `DELETE` token, and vice versa.

### Post Data
In order to post the data, you will need to use JSON with the following keys:
1. `country`
2. `gid_0` - ISO3 country code
3. `gid_1` - Admin 1 level code
3. `date` - YYYY/MM format
4. `outcome` - Indicator name
5. `predicted` - predicted value
6. `predicted_error` - predicted error

If all of these headers and values are not present, the request will be rejected. If there are rows in the database matching `country`, `gid_0`, `date` and `outcome`, the request will be rejected to prevent duplication.
A single row example to be posted to the database, would be:

```json
[{'country': 'Afghanistan', 'gid_0': 'AFG', 'gid_1': 'AFG.1_1', 'date': '2024-08', 'outcome': 'mobile_women', 'predicted': 30.0, 'predicted_error': 5.6}]
```

Multiple rows can be posted at the same time (in an array matching the above format).

### Delete Data
In order to delete the data, you will need to use JSON with the following keys:
1. `country`
2. `gid_0` - ISO3 country code
3. `gid_1` - Admin 1 level code
3. `date` - YYYY/MM format
4. `outcome` - Indicator name
5. `predicted` - predicted value
6. `predicted_error` - predicted error

If all of these headers and values are not present, the request will be rejected. If there are rows in the database matching `country`, `gid_0`, `date` and `outcome`, the request will be rejected.
A single row example to be deleted from the database, would be:

```json
[{'country': 'Afghanistan', 'gid_0': 'AFG', 'gid_1': 'AFG.1_1', 'date': '2024-08', 'outcome': 'mobile_women', 'predicted': 30.0, 'predicted_error': 5.6}]
```

## Deleting and posting utility scripts
In the same `./scripts` folder as above, there are utility scripts that can be run to delete or post small edits to the database. You will not be able to delete full tables. In these cases, it would be better to `ssh` into the server machine and delete the tables using `psql`:
**NOTE** PLEASE RUN THE BELOW COMMAND WITH CAUTION
```ssh
PGPASSWORD=XXXXXXXXXXXXX psql -h localhost -p 5432 -U oxford_dgg_admin -d dgg -c "DELETE FROM national_indicators;"
``` 
You will need to get the password from the `.env` file in the application root.

1. `python ./scripts/delete_national.py` - You will need to copy a csv into the scripts folder detailing the rows you would like deleted, and update the `CSV` attribute pointing to the csv path.
2. `python ./scripts/delete_subnational.py` - You will need to copy a csv into the scripts folder detailing the rows you would like deleted, and update the `CSV` attribute pointing to the csv path.
3. `python ./scripts/post_national.py` - You will need to copy a csv into the scripts folder detailing the rows you would like posted to the database, and update the `CSV` attribute pointing to the csv path.
4. `python ./scripts/post_subnational.py` - You will need to copy a csv into the scripts folder detailing the rows you would like posted to the database, and update the `CSV` attribute pointing to the csv path.

## API Client and automation scripts
**NOTE These scripts are not intended for large data insertions. Please do not attempt to bulk insert more than one month at a time to prevent timeout errors. See below for bulk-insert scripts**
In addition to the above, there is a client class in the `./scripts/` directory that helps to automate the posting, deleting and backing up of data. To carry out these tasks, you will need to edit `./scripts/post_and_backup.py`.
1. Point the script to the location of your env file:
```python
BASE_DIR = Path(__file__).resolve().parent.joinpath('data')
ENV = BASE_DIR.parent.joinpath('.env')
```
2. Set the root_url to point to the API:
```python
root_url = "http://3.11.85.207/api/v2"
```
3. Point the script to the directories holding the csv's to post for subnational and national data. These folders SHOULD BE CREATED BUT CAN BE EMPTY if one or the other level is available **NOTE - The post data should be replaced each time you make a post**:
```python
post_national_level_dir = BASE_DIR.joinpath("post/national")
post_subnational_level_dir = BASE_DIR.joinpath("post/subnational")
```
3. Point the script to the directories holding the csv's to delete for subnational and national data. These folders SHOULD BE CREATED BUT CAN BE EMPTY if one or the other level is available. **NOTE - The post data should be replaced each time you make a post**:
```python
delete_national_level_dir = BASE_DIR.joinpath("delete/national")
delete_subnational_level_dir = BASE_DIR.joinpath("delete/subnational")
```
The delete function is option and is flagged to not delete by default. You will need to change the parameters passed to the `main` function to set the script to delete
```python
# Change to True for levels you would like to delete (using csvs)
main(delete_national=False, delete_subnational=False)
```
4. Point the script to a folder in which to save errors. If there are duplicates or invalid requests, the rows of the input csv will be saved to this csv. This csv will be suffixed with the date/time that it was saved:
```python
errors_csv_dir = BASE_DIR.joinpath("errors")
```
5. Point the script to the folder in which to save national and subnational backup csvs from the database. These will be suffixed with the date/time that it was saved. This folder may need some tidying up after some time to save space.
```python
backup_dir = BASE_DIR.joinpath("backup")
```

Running the script will try to post the data in the respective levels' directories, save a backup for each level, and then if set, will delete the data in the delete directories. If you would like to delete BEFORE backing up, the code:
```python
if delete_national:
        client.delete_national_data()
    if delete_subnational:
        client.delete_subnational_data()
```
should be placed above 
```python
client.create_backup()
```
The `./script/data` folder has all the necessary folders needed to run the script, and you will just need to add the csv's to the folders in which they belong.

## Bulk insert script
This script is intended for large insertions. You will need to harmonise the data that you would like to insert with the data already in the database - this script will DELETE all rows the table you are inserting to, and will replace the data with the csv that you specify. Use with caution as there is no validation.

1. Using ssh, copy the csv that you would like to replace in the database in the corresponding `./scripts/data/post/<national or subnational>` directory on the server machine. This will ONLY work with 1 csv. Please do not use this script with more than one csv in the directory.
For example:
`scp ./scripts/data/post/national/dgg_national_combined_cleaned.csv ubuntu@13.41.46.70:/dgg-www/scripts/data/post/national/`
2. Run `python ./scripts/reinsert_all_data.py`.
If there is not data in the national/subnational folders, it will be skipped. There is no need to delete data from the database with this script as it will be deleted in the script. This script does not create a backup of the table. You will need to do this manually.
**PLEASE REMEMBER TO DELETE CSVS FROM THE SERVER MACHINE AFTER THIS PROCESS**


## Testing

### Stress/Load Testing
Some simple stress/load test scripts have been written in the `./api/tests/stress/` directory, `k6-scripts.js` for simple tests, `k6-script-heavy` for requests getting larger responses. The scripts will be run in the CI/CD pipeline when a branch is pushed to the repo (defined in `./.github/workflows/ci.yaml`). See [Grafana Docs](https://grafana.com/docs/k6/latest/get-started/results-output/) for an explanation on how to interpret the output.

You will need Docker installed to run the tests locally. Change directory to `./api/tests/stress/`, and run `docker-compose up --build`. Output will be displayed in the terminal.

The tests are set up to ramp up to a desired number of users over a specified time, hold that number for a specified time, and then ramp down for a specified time in the `stages` array in the `options` object in the scripts:

```javascript
stages: [
        { duration: '20s', target: 20 }, // ramp up to 50 users over 20 seconds
        { duration: '180s', target: 20 }, // hold at 50 users for 30 seconds
        { duration: '20s', target: 0 },  // ramp down to 0 users over 10 seconds
    ],
```
The durations and target are probably the only values that need to be changed, but please be careful how you push these values to github, as the pipelines will fail if the tests fail, resulting in the branch merges to main being disabled. 

The tests can be disabled by removing the `k6-test` element in the `jobs` section of the `./.github/workflows/ci.yaml` file, or by deleting the `workflows` directory in the `./.github/` folder.

