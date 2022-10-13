---
title: API Docs
output: rmdformats::readthedown
---

# Digital Gender Gaps API (v1)

The Digital Gender Gaps API allows you to access all data displayed at **digitalgendergaps.org**. 
This provides a way to automate data requests for individual countries, specific dates, or bulk downloads. 
We aim to update our data once per month and to make them openly available for free. 
Web developers can use this API to develop web applications that query our database on-the-fly based on the needs of your 
users.

## Overview of all endpoints

**./api/v1/init**  
Returns data needed to initialize the web application.

**./api/v1/query_specific_country**  
Returns digital gender gap estimates for all dates for a single country. See below for a list of required 
arguments. 

**./api/v1/query_national**  
Returns digital gender gap estimates for all countries for a single date. See below for a list of required 
arguments.

**./api/v1/download_data_with_dates**  
Returns digital gender gap estimates for all countries within a range of dates. See below for a list of required 
arguments.

**./api/v1/write_national**  
Writes new digital gender gap estimates into the database for a single country and date. See below for a list of 
required arguments.


## Endpoint: init
Returns data needed to initialize the web application including:  
- A list of countries with data  
- A list of dates with data  
- Descriptions of each indicator used to measure digital gender gaps  
- Types of indicators (e.g. mobile phone access, internet access)  
- Colour palette for mapping results  
- Contact email address  

**Example query**  
<a href="http://digitalgendergaps.org/api/v1/init" target="_blank">`http://digitalgendergaps.org/api/v1/init`</a>

> **Note:** Click the link above and paste the JSON response <a href="https://duckduckgo.com/?q=json+beautifier" target="_blank">here</a> to view 
it in a cleaner format.

**Arguments**  
None

**Response**  
The JSON response includes the following elements:  

| Response  | Description | 
|---|---|
| countries | A list of all countries with data. This includes country names and ISO2 country codes. |   
| dates     | A list of dates with data formatted as YYYYMM. |               
| models    | An object containing descriptions of all indicators (i.e. models) including their name, formatted name, type, description, and display order. | 
| types     | A list of indicator types (e.g. mobile, internet).|  
| palette   | Colour palette for mapping results including colour hex codes, break point, legend title, subtitles, and labels. |  
| contact   | A contact email address. |
| status    | http status code. |
| message   | Status message. |


## Endpoint: query_specific_country
Returns data for all dates from a single country.

**Example queries**  
<a href="http://digitalgendergaps.org/api/v1/query_specific_country?iso2code=GB" target="_blank">`http://digitalgendergaps.org/api/v1/query_specific_country?iso2code=GB`</a>  

<a href="http://digitalgendergaps.org/api/v1/query_specific_country?iso2code=GB&model=['internet_online_model_prediction']" target="_blank">`http://digitalgendergaps.org/api/v1/query_specific_country?iso2code=GB&model=['internet_online_model_prediction']`</a>

> **Note:** Click the links above and paste the JSON responses <a href="https://duckduckgo.com/?q=json+beautifier" target="_blank">here</a> to view them in a cleaner format.

**Arguments**  
| Argument | Description |
|---|---|
| iso2code | (required) Country as a two character <a href="https://en.wikipedia.org/wiki/ISO_3166-2" target="_blank">ISO-2 country code</a>. |
| model | (optional) List of indicators to return. Note: Get possible values from keys of the "model" element returned from the "init" endpoint. | 

**Response**  
The JSON response includes the following elements:  

| Response | Description  |
|---|---|
| data | Digital gender gap estimates for each indicator and date. | 
| status   | http status code.  |
| message  | Status message. |


## Endpoint: query_national
Returns data for all countries for a single date.

**Example queries**  
<a href="http://digitalgendergaps.org/api/v1/query_national?date=202206" target="_blank">`http://digitalgendergaps.org/api/v1/query_national?date=202206`</a>

<a href="http://digitalgendergaps.org/api/v1/query_national?date=202206&model=['internet_online_model_prediction']" target="_blank">`http://digitalgendergaps.org/api/v1/query_national?date=202206&model=['internet_online_model_prediction']`</a>

> **Note:** Click the links above and paste the JSON responses <a href="https://duckduckgo.com/?q=json+beautifier" target="_blank">here</a> to view them in a cleaner format.

**Arguments**  
| Argument | Description  |
|---|---|
| date | (required) Date in format YYYYMM.  |                                                                  
| model | (optional) List of indicators to return. Note: Get possible values from keys of the "model" element returned from the "init" endpoint. | 

**Response**  
The JSON response includes the following elements:  

| Response | Description  |
|---|---|
| data | Digital gender gap estimates for each indicator and date. |
| message  | Status message. |                                            
| status   | http status code. |


## Endpoint: download_data_with_dates
Returns data for all countries within a range of dates.

**Example query**  
<a href="http://digitalgendergaps.org/api/v1/download_data_with_dates?start_date=202206&end_date=202207" target="_blank">`http://digitalgendergaps.org/api/v1/download_data_with_dates?start_date=202206&end_date=202207`</a>

> **Note:** Click the link above and paste the JSON response <a href="https://duckduckgo.com/?q=json+beautifier" target="_blank">here</a> to view it in a cleaner format.

**Arguments**  
| Argument   | Description | 
|---|---|
| start_date | (required) Initial date in range in format YYYYMM. |
| end_date   | (required) Last date in range in format YYYYMM.    |     


**Response**  
The JSON response includes the following elements:  

| Response | Description  |
|---|---|
| data | Digital gender gap estimates for each country, date, and indicator. |
| message  | Status message.  |
| status   | http status code. |


## Endpoint: write_national
Writes new digital gender gap estimates into the database for a single country and date.

**Example query**  
<a href="http://digitalgendergaps.org/api/v1/write_national?token=XXXXX&iso2=GB&date=202210&Ground_Truth_Internet_GG=0.5" target="_blank">`http://digitalgendergaps.org/api/v1/write_national?token=XXXXX&iso2=GB&date=202210&Ground_Truth_Internet_GG=0.5`</a>


> **Note:** This endpoint requires an access token and is not available for public access.

**Arguments**  
| Argument | Description | 
|---|---|
| token | (required) Access token.  |
| date | (required) Date in format YYYYMM. |  
| iso2 | (required) Country as a two character <a href="https://en.wikipedia.org/wiki/ISO_3166-2" target="_blank">ISO-2 country code</a>.| | internet_online_model_prediction | (optional) Value to write into database for this indicator. |
| internet_online_offline_model_prediction | (optional) Value to write into database for this indicator. |
| internet_offline_model_prediction        | (optional) Value to write into database for this indicator. |
| ground_truth_internet_gg                 | (optional) Value to write into database for this indicator. |
| mobile_online_model_prediction           | (optional) Value to write into database for this indicator. |
| mobile_online_offline_model_prediction   | (optional) Value to write into database for this indicator. |
| mobile_offline_model_prediction          | (optional) Value to write into database for this indicator. |
| ground_truth_mobile_gg                   | (optional) Value to write into database for this indicator. |

**Response**  
The JSON response includes the following elements:  

| Response | Description | 
|---|---|
| data | Digital gender gap estimates for each country, date, and indicator.  | 
| message | Status message. |  
| status | http status code. |  


## Query API from Python or R

### Python

```{python}
# import packages
import requests
import pandas as pd

# query arguments
args = {
  "iso2code": "AT"
  }

# submit query as GET request
response = requests.get(url = 'http://digitalgendergaps.org/api/v1/query_specific_country', 
                        params = args)

# format response as dictionary
response = response.json()

# check status
print(response.get('status'))
print(response.get('message'))

# extract data as pandas dataframe
if response.get('status') == 200:
  data = pd.DataFrame(json.loads(response.get('data')))
```

### R

```{r}
# import packages
library('httr')
library('jsonlite')
options(scipen = 999)

# query arguments
args <- list(iso2code = "AT")

# submit query as GET request
response <- httr::GET(url = 'http://digitalgendergaps.org/', 
                      path = 'api/v1/query_specific_country',
                      query = args)

# format response as list
response <- jsonlite::fromJSON(httr::content(response, as='text'))

# check status
print(response$status)
print(response$message)

# extract data in various formats
if(response$status == 200){
  
  # json string
  data <- response$data
  
  # json -> list of lists
  data <- jsonlite::fromJSON(data)
  
  # list of lists -> data.frame with cells containing lists
  # note: this is a convenient format for dealing with JSONs for some data.frame cells in R.
  data <- as.data.frame(do.call(cbind, data))
  
}
```
