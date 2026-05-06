import gspread
from google.oauth2.service_account import Credentials
import os
import json
from dotenv import load_dotenv
o
load_dotenv()

def get_sheet():
    # Define the scope for Google Sheets and Drive APIs
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Authenticate using the service account
    # Prioritize environment variable for deployment (Railway), fallback to file for local
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if creds_json:
        info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(info, scopes=scope)
    else:
        creds = Credentials.from_service_account_file("credentials.json", scopes=scope)

    client = gspread.authorize(creds)

    # Open the sheet by its ID from the .env file
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    return client.open_by_key(sheet_id).get_worksheet(0)

def append_job_row(data):
    """
    Appends a new row to the Google Sheet.
    data: List of values [Company, Program/Role, Deadline, Applied?, Status, Application Url]
    """
    sheet = get_sheet()
    sheet.append_row(data)
