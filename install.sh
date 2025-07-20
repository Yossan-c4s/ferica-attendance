#!/bin/bash
set -e

sudo apt update
sudo apt install -y python3 python3-pip python3-venv unclutter matchbox-window-manager chromium-browser

# 仮想環境作成
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "インストール完了。config/credentials.json を設置して下さい。"
echo "Raspberry Pi再起動で自動起動します。"
