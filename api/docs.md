# Digital Gender Gaps API (v1)

> Query data measuring monthly digital gender gaps for countries globally. 

## Endpoints

**digitalgendergaps.org/api/v1/init**  
Returns the list of countries and dates with data along with the names of various models used to predict digital gender gaps.

**digitalgendergaps.org/api/v1/query_country**  
Returns digital gender gap estimates for a select country.


## Arguments

The 'init' endpoint does not require any arguments.  

The other endpoints will all accept the arguments described below.  

Argument | Description 
|---|---|
iso2code | ISO-2 country code. 

## API Response
The API will return a json response with five elements:

Element | Description
|---|---| 
status | http status code
message | Message describing outcome of operation writing to the database
timestamp | Date and time of response
data | Data resulting from query in json format

For example:
```{python}
{
  "status": 200,
  "message": "OK: Data successfully selected from database.",
  "timestamp": "2022-01-03 18:30:26+00",
  "data": '{"data":"{\"region\":{\"0\":\"BOLIVIA\",\"1\":\"BRUNEI\",...'
}
```


## Examples

**Query data using a url:**  
```{python}
http://digitalgendergaps.org/api/v1/query_national?iso2code=AT
```

**Query data from Python:**
```{python}
# import packages
import requests
import pandas as pd

# query arguments
args = {
  "iso2code": "AT"
  }

# submit query as GET request
response = requests.get(url = 'http://digitalgendergaps.org/api/v1/query_national', 
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

**Query data from R:**
```{r}
# import packages
library('httr')
library('jsonlite')
options(scipen = 999)

# query arguments
args <- list(iso2code = "AT")

# submit query as GET request
response <- httr::GET(url = 'http://digitalgendergaps.org/', 
                      path = 'api/v1/query_country',
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





