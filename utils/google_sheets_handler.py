# utils/google_sheets_handler.py

import gspread
from google.oauth2.service_account import Credentials

def get_gsheet_client():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_file(
        "path/to/your/service_account.json", scopes=scopes
    )
    client = gspread.authorize(credentials)
    return client

def append_to_sheet(sheet_id, worksheet_name, data_dict):
    client = get_gsheet_client()
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)

    # Convert dictionary to row
    row = [data_dict.get(col, "") for col in worksheet.row_values(1)]
    worksheet.append_row(row)
