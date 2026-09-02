from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

# --- ตั้งค่า JSONBin ---
BIN_ID = "6a97bfeaf5f4af5e295fa090"
API_KEY = "เอา_MASTER_KEY_ที่ขึ้นต้นด้วย_$2a$10$_มาวางตรงนี้" 
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

@app.route('/api/messages', methods=['GET'])
def get_messages():
    try:
        # ดึงข้อมูลจากฐานข้อมูล
        req = requests.get(URL, headers=HEADERS)
        data = req.json()
        messages = data.get("record", {}).get("messages", [])
        
        # กรองเฉพาะข้อความที่ไม่เกิน 24 ชั่วโมง (86,400,000 มิลลิวินาที)
        now = int(time.time() * 1000)
        valid_messages = [m for m in messages if (now - m.get("timestamp", 0)) < 86400000]
        
        # พลิกกลับให้ข้อความใหม่ล่าสุดอยู่ข้างบน
        return jsonify(valid_messages[::-1])
    except Exception as e:
        return jsonify([]), 500

@app.route('/api/messages', methods=['POST'])
def add_message():
    try:
        new_msg = request.json
        new_msg["timestamp"] = int(time.time() * 1000)
        
        # 1. ดึงข้อความเดิมมาเก็บไว้ก่อน
        req = requests.get(URL, headers=HEADERS)
        data = req.json()
        messages = data.get("record", {}).get("messages", [])
        
        # 2. เอาข้อความใหม่ไปต่อท้าย
        messages.append(new_msg)
        
        # 3. บันทึกกลับไปที่ JSONBin
        requests.put(URL, json={"messages": messages}, headers=HEADERS)
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# สำหรับรันบน Vercel ไม่ต้องใช้ app.run()
