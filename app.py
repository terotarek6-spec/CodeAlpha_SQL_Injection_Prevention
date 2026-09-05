from flask import Flask, request, jsonify
import sqlite3
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)

AES_KEY = b'CodeAlpha_AES256_SecureKey_2026!' 
CAPABILITY_CODE = "ALPHA-SECURE-2026"  

def encrypt_data(data):
    """تشفير البيانات باستخدام AES-256"""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data.encode()) + encryptor.finalize()
    return base64.b64encode(iv + encrypted).decode('utf-8')

def init_db():
    """تهيئة قاعدة بيانات SQL خفيفة"""
    conn = sqlite3.connect('secure_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, encrypted_info TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/add-secure-data', methods=['POST'])
def add_secure_data():
   
    provided_code = request.headers.get('X-Capability-Code')
    if provided_code != CAPABILITY_CODE:
        return jsonify({
            "status": "Access Denied", 
            "message": "Invalid Capability Code. Server access blocked to prevent unauthorized injection."
        }), 403

    data = request.json
    username = data.get('username')
    sensitive_info = data.get('sensitive_info') # مثل كلمات المرور أو أرقام الهواتف
    
    if not username or not sensitive_info:
        return jsonify({"status": "Error", "message": "Missing username or sensitive_info"}), 400

    # تشفير البيانات الحساسة قبل الحفظ
    encrypted_info = encrypt_data(sensitive_info)
    try:
        conn = sqlite3.connect('secure_database.db')
        c = conn.cursor()
        
        c.execute("INSERT INTO users (username, encrypted_info) VALUES (?, ?)", (username, encrypted_info))
        conn.commit()
        conn.close()
        
        return jsonify({
            "status": "Success",
            "message": "Data AES-256 encrypted and securely stored. SQL Injection prevented.",
            "encrypted_preview": encrypted_info
        }), 201
        
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)