from flask import Flask, jsonify
from datetime import datetime
import random
import threading
import time
import pyodbc
import os


app = Flask(__name__)

DB_SERVER = os.environ["DB_SERVER"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD};Encrypt=no;TrustServerCertificate=yes"

## Create table
def init_db():
      with pyodbc.connect(connection_string, autocommit=True) as conn:
            cursor = conn.cursor()
            cursor.exectue("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='SensorData')
            CREATE TABLE SensorData (
                DeviceId NVARCHAR(50),
                Tempaerature FLOAT,
                Humidity FLOAT,
                CreatedAt DATETIME
            )
            """)
init_db()

# Insert dummy data
def insert_fake_data():
      devices = ["Device1", "Device2", "Device3"]
      while True:
            with pyodbc.connect(connection_string, autocommit=True) as conn:
                  cursor = conn.cursor()
                  for device in devices:
                        temp = round(random.uniform(20, 30), 2)
                        hum = round(random.uniform(30, 60), 2)
                        cursor.execute("INSERT INTO SensorData VALUES (?, ?, ?, ?)",
                                       device, temp, hum, datetime.now())
            time.sleep(5)

threading.Thread(target=insert_fake_data, daemon=True).start()

@app.route("/data")
def get_data():
    with pyodbc.connect(connection_string) as conn:
          cursor = conn.cursor()
          cursor.execute("SELECT TOP 100 * FROM SensorData ORDER BY CreatedAt DESC")
          rows = cursor.fetchall()
          result = []
          for row in rows:
                result.append({
                      "DeviceId": row[0],
                      "Temperature": row[1],
                      "Humidity": row[2],
                      "CreatedAt": row[3].strftime("%Y-%m-%d %H:%M:%S")
                })
    return jsonify(result)

if __name__ == "__main__":
        app.run(host="0.0.0.0", port=80)
        