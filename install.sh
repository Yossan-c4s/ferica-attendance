#!/bin/bash
set -e

sudo apt update
sudo apt install -y python3 python3-pip unclutter matchbox-window-manager chromium-browser
sudo pip3 install --upgrade pip
pip3 install -r requirements.txt

# udevルールでカードリーダー自動認識例（必要に応じてカスタマイズ）

echo "インストール完了。config/credentials.json を設置して下さい。"
echo "Raspberry Pi再起動で自動起動します。"