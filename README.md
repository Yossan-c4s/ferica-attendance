# Fericaカードによる出退勤管理システム

## 概要

Raspberry Pi 5・SONY RC-S380・OSOYOO 5インチDSIタッチパネルを組み合わせ、Fericaカードで出退勤管理を行うシステムです。Googleスプレッドシートをデータベースとして利用し、装置ごとの打刻情報をリアルタイムに集約します。

---

## システム構成図

![system_diagram](docs/system_diagram.png)

---

## 必要機器・環境

- Raspberry Pi 5 (Raspberry Pi OS最新版) 2台
- SONY RC-S380 カードリーダー 2台
- OSOYOO 5inch DSI Touch Screen 2台
- Wi-Fi（SSID: testssid1234, PASS: password1234）
- Googleアカウント（GoogleスプレッドシートAPI利用）

---

## セットアップ手順

### 1. リポジトリクローン

```bash
git clone https://github.com/your-org/ferica-attendance-system.git
cd ferica-attendance-system
```

### 2. インストーラー実行

```bash
sudo bash install.sh
```

### 3. Google API 設定

1. [Google Cloud Console](https://console.cloud.google.com/) で新規プロジェクトを作成
2. 「Google Sheets API」「Google Drive API」を有効化
3. サービスアカウントを作成し、「編集者」権限を付与
4. サービスアカウントの JSON キーを `config/credentials.json` として保存
5. Googleスプレッドシートを新規作成し、`config/config.yaml` の `spreadsheet_id` に設定
6. スプレッドシート共有設定でサービスアカウントのメールアドレスに"編集者"権限付与

### 4. Raspberry Pi 装置ID設定

`config/config.yaml` の `device_id` を装置ごとに `RAS01` `RAS02` へ書き換える

---

## 起動・運用

- Raspberry Piの電源ONで自動起動
- カードをかざすと画面に氏名・時刻表示（5秒間 or 連続割込表示）
- 午前中は「出勤」、午後は「退勤」に自動切替
- 「出勤」「退勤」ボタンで手動切替可能（10秒後に自動リセット）
- 未登録カードは「未登録ユーザー」として自動登録

---

## ディレクトリ構成

```
ferica-attendance-system/
├── app/
│   ├── main.py
│   ├── reader.py
│   ├── sheets.py
│   ├── gui/
│   │   ├── index.html
│   │   ├── style.css
│   │   ├── app.js
│   │   └── icon.png
│   └── utils.py
├── config/
│   ├── config.yaml
│   └── credentials.json
├── install.sh
├── docs/
│   └── system_diagram.png
└── README.md
```

---

## Googleスプレッドシート 構成例

### シート1: users

| user_id | name          | card_id        |
|---------|---------------|---------------|
| 0001    | 山田太郎      | 0123456789AB  |
| 0002    | 佐藤花子      | 1234567890CD  |
| ...     | ...           | ...           |

### シート2: attendance

| timestamp           | name          | card_id      | device_id | type   |
|---------------------|---------------|--------------|-----------|--------|
| 2025/07/20 08:45:00 | 山田太郎      | 0123456789AB | RAS01     | 出勤   |
| 2025/07/20 17:35:10 | 佐藤花子      | 1234567890CD | RAS02     | 退勤   |
| ...                 | ...           | ...          | ...       | ...    |

---

## ライセンス

MIT
