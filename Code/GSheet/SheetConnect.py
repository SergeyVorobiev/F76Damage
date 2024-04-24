import gspread
from gspread import Spreadsheet, WorksheetNotFound

import Root


class SheetConnect:

    @staticmethod
    def get_spreadsheet(config, spreadsheet_name) -> Spreadsheet:

        file_name = config.get_string("GSheet", "Credentials") + ".json"
        return gspread.service_account(Root.build_resources_path(("Creds", file_name))).open(spreadsheet_name)

    @staticmethod
    def get_or_create_sheet(sheet_name, spreadsheet, error_message=None):
        try:
            sheet = spreadsheet.worksheet(sheet_name)
        except WorksheetNotFound:
            if error_message is not None:
                print(error_message)
            sheet = spreadsheet.add_worksheet(sheet_name, 1000, 10)
        return sheet
