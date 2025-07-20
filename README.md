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
git clone https://github.com/ferica-attendance/ferica-attendance-system.git
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

### 3. Google API 設定（初心者向け詳細手順）

このシステムはGoogleスプレッドシートをデータベースとして利用します。Google Sheets APIを使うための設定手順を詳しく説明します。

#### 3-1. Googleアカウントを準備する

Googleアカウントをお持ちでない場合は、[Googleアカウント作成ページ](https://accounts.google.com/signup)から作成してください。

---

#### 3-2. Google Cloud Platform (GCP) でプロジェクトを作成

1. [Google Cloud Platform（GCP）コンソール](https://console.cloud.google.com/)にアクセスし、Googleアカウントでログインします。
2. 画面右上の「プロジェクトの選択」から「新しいプロジェクト」をクリックします。
3. プロジェクト名を入力（例：`FericaAttendance`）し、「作成」をクリックします。
4. 左上の「ナビゲーションメニュー」から「APIとサービス」>「ダッシュボード」を開き、作成したプロジェクトが選択されていることを確認します。

---

#### 3-3. Google Sheets API、Google Drive APIを有効化する

1. 「APIとサービス」>「ライブラリ」をクリックします。
2. 検索窓で「Google Sheets API」と入力し、表示されたAPIをクリックします。
3. 「有効にする」を押します。
4. 続けて「Google Drive API」も同様に検索・有効化します。

---

#### 3-4. サービスアカウントを作成し、認証情報をダウンロード

1. 「APIとサービス」>「認証情報」をクリックします。
2. 「認証情報を作成」→「サービスアカウント」を選択します。
3. サービスアカウント名を入力（例：`ferica-attendance-service`）、必要なら説明も入力し、「作成して続行」。
4. 「ロールを選択」で「編集者」を選択します（`基本`→`編集者`）。
5. 続行し、完了まで進みます。
6. 作成したサービスアカウントが一覧に表示されるので、該当の行の右端「︙」→「キーを管理」をクリック。
7. 「キーを追加」→「新しいキーを作成」→「JSON」形式を選択し、「作成」。
8. `credentials.json` という名前のファイルが自動的にダウンロードされます。

---

#### 3-5. 認証ファイルを設置

ダウンロードした `credentials.json` ファイルを、システムの `config/` フォルダ内にコピーします。

例：  
```bash
cp ~/Downloads/credentials.json ferica-attendance-system/config/credentials.json
```

---

#### 3-6. Googleスプレッドシートを新規作成

1. [Googleスプレッドシート](https://docs.google.com/spreadsheets/)にアクセスし、「新しいスプレッドシートを作成」。
2. ファイル名を分かりやすいもの（例：`FericaAttendanceDB`）に変更。
3. URLの`/d/`と`/edit`の間にある文字列が「スプレッドシートID」です。例：
   ```
   https://docs.google.com/spreadsheets/d/【この部分がID】/edit#gid=0
   ```
4. このIDを `config/config.yaml` の `spreadsheet_id:` にコピペしてください。

---

#### 3-7. スプレッドシートにシートを作成

1. スプレッドシート下部の「+」ボタンで「users」「attendance」という2つのシート（タブ）を作成します。
2. それぞれ以下のように1行目にカラム名を入力してください。

##### `users`シート  
| user_id | name | card_id |

##### `attendance`シート  
| timestamp | name | card_id | device_id | type |

---

#### 3-8. サービスアカウントに編集権限を付与

1. 「credentials.json」内の`client_email`フィールド（例：`ferica-attendance-service@xxxx.iam.gserviceaccount.com`）をコピー。
2. 作成したスプレッドシートを開き、右上の「共有」ボタンをクリック。
3. 「ユーザーやグループを追加」に上記メールアドレスを貼り付け、「編集者」に設定し、「送信」。

---

#### 3-9. 完了

これでGoogle Sheets APIの設定は完了です。  
インストール手順に従い、システムを起動してください。

---

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
