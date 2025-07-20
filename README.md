# Fericaカードによる出退勤管理システム

## システム概要

Raspberry Pi 5 ＋ SONY SR-380カードリーダー＋OSOYOO 5インチDSIタッチパネルで構成される、Fericaカードによる出退勤管理システムです。出退勤情報はGoogle Spreadsheetをデータベースとして蓄積します。

## 主な特徴

- Raspberry Pi起動時に自動でシステムが起動、フルスクリーンWeb UIで操作可能
- Fericaカードをかざすと氏名・時刻が即座に表示され、5秒後に消去（割り込み可）
- 未登録カードは「未登録ユーザー」として自動登録
- 午前は「出勤」、午後は「退勤」自動判定。ボタンで手動切替も可能
- 2台のPiを用意し、装置IDで区別
- Google Spreadsheetをデータベースとして利用
- GitHubからそのままPullしてセットアップ可能な構成
- インストールシェルスクリプト付属

## 構成図

```
[User] --(Fericaカード)--> [SR-380カードリーダ] --USB--> [Raspberry Pi 5] --WiFi--> [Google Spreadsheet]
                                                  |
                                        [OSOYOO 5" Touch Panel]
```

## ファイル構成

```
/
├── README.md
├── installer.sh
├── src/
│   ├── app.py                  # サーバー本体 (Flask)
│   ├── card_reader.py          # Fericaカードリーダ処理
│   ├── google_sheets.py        # Google Sheets連携
│   ├── config.py.template      # 設定ファイルのテンプレート
│   ├── static/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── app.js
│   └── systemd/
│       └── ferica-attendance.service
└── requirements.txt
```

## セットアップ手順

1. **GitHubリポジトリをClone**

   ```
   git clone https://github.com/YourOrg/ferica-attendance.git
   cd ferica-attendance
   ```

2. **インストーラー実行**

   ```
   chmod +x installer.sh
   sudo ./installer.sh
   ```

3. **Google API認証ファイル配置**

   - `src/google_sheets.py`の指示に従い、Google Cloud PlatformでAPIキーを取得し、`credentials.json`を`src/`に配置

4. **config.py作成**

   - `src/config.py.template`をコピーし、`src/config.py`を作成
   - `DEVICE_ID`（例：RAS01, RAS02）、Wi-Fi情報などを記入

5. **自動起動設定（systemd）**

   ```
   sudo cp src/systemd/ferica-attendance.service /etc/systemd/system/
   sudo systemctl enable ferica-attendance
   sudo systemctl start ferica-attendance
   ```

6. **Raspberry Pi起動時に自動起動し、タッチパネルでシステム利用開始**

## 必要なパッケージ

- Python 3.11+
- Flask
- pyserial
- gspread, google-auth
- その他requirements.txt参照

## 使用上の注意

- 各Piには固有の`DEVICE_ID`を設定してください
- Google Spreadsheetの編集権限が必要です
- タッチパネル用にUIは1024x600など5インチ向けに最適化

## ライセンス

MIT
