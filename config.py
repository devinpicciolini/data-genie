import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import psycopg2

# OpenAI API credentials
openai.api_key = "YOUR API KEY HERE"

# OpenAI engine and settings
ENGINE = "text-davinci-002"
TEMPERATURE = 0.4
MAX_TOKENS = 500

# Connect to Google Sheets API
def connect_to_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client

# Set up database connection
def connect_to_db():
    conn = psycopg2.connect(
        database="your db",
        user="your user",
        password="your password",
        host='localhost',
        port='your db port'
    )
    return conn

# Input messages
SHEET_PROMPT = "Please enter the URL of the Google Sheet: "
SHEET_NAME_PROMPT = "Please enter the sheet name: "
FILE_PROMPT = "Please enter the file path: "
SOURCE_PROMPT = "Would you like to use a Google Sheet or a local file as your data source? (Sheet/File) "
INVALID_SOURCE_PROMPT = "Invalid source. Please enter 'Sheet' or 'File'."

# Query prompt
QUERY_PROMPT = "Write a query that will fulfill the user's request of '{}' using the table '{}' with the following table structure: {}. Make sure to handle missing data or null values and consider more complex queries. Respond with only a SQL query, no explanation."
