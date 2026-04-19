import pandas as pd
from flask import Flask, jsonify, request
import threading
import time
import os
import datetime

app = Flask(__name__)

latest_data = {}
CSV_FILE = "data.csv"
REFRESH_INTERVAL = 5


# 🔁 Read CSV continuously (fallback mode)
def read_csv_continuously():
    global latest_data

    while True:
        try:
            if not os.path.exists(CSV_FILE):
                print("CSV file not found")
                time.sleep(REFRESH_INTERVAL)
                continue

            df = pd.read_csv(CSV_FILE)

            if df.empty:
                raise ValueError("CSV is empty")

            row = df.iloc[0]

            latest_data = {
                "status": "success",
                "source": "csv",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data": row.to_dict()
            }

        except Exception as e:
            latest_data = {
                "status": "error",
                "message": str(e)
            }

        time.sleep(REFRESH_INTERVAL)


# 🚀 START THREAD (important for Render)
thread = threading.Thread(target=read_csv_continuously, daemon=True)
thread.start()


# 📡 GET API (mobile app will use this)
@app.route('/data', methods=['GET'])
def get_data():
    if not latest_data:
        return jsonify({
            "status": "error",
            "message": "No data available yet"
        }), 503

    return jsonify(latest_data)


# 🔥 POST API (PC will send live data here)
@app.route('/update', methods=['POST'])
def update_data():
    global latest_data

    try:
        incoming = request.json

        latest_data = {
            "status": "success",
            "source": "live",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": incoming
        }

        return jsonify({"message": "Data updated successfully"})

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# 🏠 Home check
@app.route('/')
def home():
    return "Plant Monitor API Running 🚀"
