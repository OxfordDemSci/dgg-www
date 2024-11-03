# Load required libraries
library(httr)
library(readr)
library(dotenv)

# Load environment variables from .env file
dotenv::load_dotenv()

# Define constants
BASE <- normalizePath(dirname(sys.frame(1)$ofile))
ENV_FILE <- file.path(BASE, "..", ".env")
ROOT_URL <- "http://3.11.85.207/api/v2"

# Function to get token
get_token <- function(username, password) {
  url <- paste0(ROOT_URL, "/login")
  response <- POST(url, body = list(username = username, password = password), encode = "json")
  stop_for_status(response)
  content(response)$access_token
}

# Function to get data
get_data <- function() {
  url <- paste0(ROOT_URL, "/get_subnational_data?date=2024-05&country=AFG")
  response <- GET(url)
  stop_for_status(response)
  content(response)
}

# Function to get CSV data
get_csv_data <- function() {
  post_csv <- file.path(BASE, "test_post_delete.csv")
  df <- read_csv(post_csv)
  as.list(df)
}

# Function to post data
post_data <- function(token) {
  data <- get_csv_data()
  url <- paste0(ROOT_URL, "/post_subnational_data")
  response <- POST(url, body = data, encode = "json", add_headers(Authorization = paste("Bearer", token)))
  stop_for_status(response)
  content(response)
}

# Function to delete data
delete_data <- function(token) {
  data <- get_csv_data()
  url <- paste0(ROOT_URL, "/delete_subnational_data")
  response <- DELETE(url, body = data, encode = "json", add_headers(Authorization = paste("Bearer", token)))
  stop_for_status(response)
  content(response)
}

# Main function
main <- function() {
  username <- Sys.getenv("POSTGRES_USER")
  password <- Sys.getenv("POSTGRES_PASSWORD")
  token <- get_token(username, password)
  
  # GET DATA
  data <- get_data()
  print(data)
  
  # POST DATA
  # This can contain an error if the data already exists
  post_response <- post_data(token)
  print(post_response)
  
  # DELETE DATA
  # You need to sign in with the DELETE USERNAME
  # This can contain an error if the data does not exist
  delete_username <- Sys.getenv("POSTGRES_DELETE_USERNAME")
  delete_password <- Sys.getenv("POSTGRES_DELETE_PASSWORD")
  delete_token <- get_token(delete_username, delete_password)
  delete_response <- delete_data(delete_token)
  print(delete_response)
}

# Run the main function
main()