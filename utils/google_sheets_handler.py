import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd

def get_gsheet_client():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_info(
        st.secrets["google_service_account"], scopes=scope
    )
    return gspread.authorize(credentials)

def append_to_sheet(sheet_id, worksheet_name, summary_data):
    client = get_gsheet_client()
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)

    # Convert dict to row (values only, ordered)
    if isinstance(summary_data, dict):
        row = [summary_data.get(key, "") for key in worksheet.row_values(1)]
        worksheet.append_row(row)
    elif isinstance(summary_data, pd.DataFrame):
        for _, row in summary_data.iterrows():
            worksheet.append_row(row.tolist())
