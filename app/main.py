import os
import time
import threading
from flask import Flask, render_template, request, jsonify
import webview
import yaml
from app.reader import FelicaReader
from app.sheets import GoogleSheets
from app.utils import get_japan_time

CONFIG = yaml.safe_load(open("config/config.yaml"))
DEVICE_ID = CONFIG["device_id"]

gs = GoogleSheets(CONFIG)

app = Flask(__name__, static_folder="gui", template_folder="gui")
last_display = {"time": 0}

@app.route("/")
def index():
    return render_template("index.html", device_id=DEVICE_ID)

@app.route("/api/punch", methods=["POST"])
def punch():
    data = request.json
    card_id = data.get("card_id")
    action = data.get("action")
    user = gs.get_or_register_user(card_id)
    now_str = get_japan_time().strftime("%Y/%m/%d %H:%M:%S")
    gs.append_attendance(now_str, user["name"], card_id, DEVICE_ID, action)
    return jsonify({"name": user["name"], "timestamp": now_str})

@app.route("/api/device_id")
def device_id():
    return jsonify({"device_id": DEVICE_ID})

def start_flask():
    app.run(host="0.0.0.0", port=5000, threaded=True)

def start_reader():
    reader = FelicaReader()
    while True:
        card_id = reader.polling_card()
        if card_id:
            now = time.time()
            if now - last_display.get("time", 0) > 1:
                last_display["time"] = now
                # 通知をWebフロントに送信する場合はWebSocket等に拡張
        time.sleep(0.1)

if __name__ == "__main__":
    threading.Thread(target=start_flask, daemon=True).start()
    time.sleep(2)
    # フルスクリーンでWebView起動
    window = webview.create_window("出退勤", "http://localhost:5000", fullscreen=True)
    webview.start()