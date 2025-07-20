import gspread
from google.oauth2.service_account import Credentials

class GoogleSheets:
    def __init__(self, config):
        scopes = ["https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive"]
        self.gc = gspread.authorize(
            Credentials.from_service_account_file("config/credentials.json", scopes=scopes)
        )
        self.spreadsheet = self.gc.open_by_key(config["spreadsheet_id"])
        self.sheet_users = self.spreadsheet.worksheet(config["sheet_users"])
        self.sheet_attendance = self.spreadsheet.worksheet(config["sheet_attendance"])

    def get_or_register_user(self, card_id):
        users = self.sheet_users.get_all_records()
        for u in users:
            if u["card_id"] == card_id:
                return u
        # 未登録カード
        row = [f"U{len(users)+1:04d}", "未登録ユーザー", card_id]
        self.sheet_users.append_row(row)
        return {"user_id": row[0], "name": row[1], "card_id": row[2]}

    def append_attendance(self, timestamp, name, card_id, device_id, action):
        self.sheet_attendance.append_row([timestamp, name, card_id, device_id, action])