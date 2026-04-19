import pandas as pd
from flask import Flask, jsonify
import threading
import time
import os
import datetime

app = Flask(__name__)

latest_data = {}
CSV_FILE = "data.csv"

REFRESH_INTERVAL = 5   # ⏱️ 5 seconds


def read_csv_continuously():
    global latest_data

    while True:
        try:
            if not os.path.exists(CSV_FILE):
                print("CSV file not found")
                time.sleep(REFRESH_INTERVAL)
                continue

            success = False

            # 🔁 Retry if file is being written
            for attempt in range(3):
                try:
                    df = pd.read_csv(CSV_FILE)

                    if df.empty:
                        raise ValueError("CSV is empty")

                    row = df.iloc[0]

                    # ✅ Add timestamp + structured data
                    latest_data = {
                        "status": "success",
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "data": row.to_dict()
                    }

                    success = True
                    break

                except Exception as e:
                    print(f"Attempt {attempt+1} failed:", e)
                    time.sleep(0.3)

            if not success:
                latest_data = {
                    "status": "error",
                    "message": "Failed to read CSV after retries"
                }

        except Exception as e:
            latest_data = {
                "status": "error",
                "message": str(e)
            }

        time.sleep(REFRESH_INTERVAL)


@app.route('/data', methods=['GET'])
def get_data():
    if not latest_data:
        return jsonify({
            "status": "error",
            "message": "No data available yet"
        }), 503

    return jsonify(latest_data)


if __name__ == '__main__':
    try:
        thread = threading.Thread(target=read_csv_continuously, daemon=True)
        thread.start()

        print("Server running at http://0.0.0.0:5000/data")

        app.run(host='0.0.0.0', port=5000, debug=True)

    except Exception as e:
        print("Startup error:", e)