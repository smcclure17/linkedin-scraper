import gspread
import pandas as pd

GOOGLE_SHEET_ID = "1L4G0mM_iti_H5burWq22g4v4jMZW-4LhX8BvnH5o_WI"


def init_service_account():
    # Using service account key, see
    # https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account
    return gspread.service_account()


def update_sheet(
    data: pd.DataFrame, worksheet_name: str, spreadsheet_id: str = GOOGLE_SHEET_ID
):
    gsheet_engine = init_service_account()
    spreadsheet = gsheet_engine.open_by_key(spreadsheet_id)

    worksheet = spreadsheet.worksheet(worksheet_name)
    # Write contents of dataframe to worksheet (I think) this overrides existing data.
    # Find a more elegant approach as needed.
    worksheet.update([data.columns.values.tolist()] + data.values.tolist())
