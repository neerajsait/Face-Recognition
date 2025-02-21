import cv2
import numpy as np
import pickle
import os
import mysql.connector
from flask import Flask, request, jsonify, render_template_string
from deepface import DeepFace

app = Flask(__name__)

# ✅ Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="neer@jsai6", 
        database="df"
    )

# ✅ Home Page
@app.route('/')
def home():
    return render_template_string('''
        <h1>Face Recognition API</h1>
        <ul>
            <li><a href="/register">Register</a></li>
            <li><a href="/login">Login</a></li>
        </ul>
    ''')

# ✅ Register Page (Frontend)
@app.route('/register', methods=['GET'])
def register_page():
    return render_template_string('''
        <h2>Register</h2>
        <input type="text" id="username" placeholder="Enter Username" required>
        <button onclick="captureImage('/register')">Register with Face</button>
        <script>
            function captureImage(url) {
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(stream => {
                        const video = document.createElement("video");
                        video.srcObject = stream;
                        video.play();
                        setTimeout(() => {
                            const canvas = document.createElement("canvas");
                            canvas.width = 640;
                            canvas.height = 480;
                            const ctx = canvas.getContext("2d");
                            ctx.drawImage(video, 0, 0, 640, 480);
                            stream.getTracks().forEach(track => track.stop());

                            canvas.toBlob(blob => {
                                const formData = new FormData();
                                formData.append("username", document.getElementById("username").value);
                                formData.append("image", blob);

                                fetch(url, { method: "POST", body: formData })
                                    .then(response => response.json())
                                    .then(data => alert(data.message))
                                    .catch(error => alert("Error: " + error));
                            }, "image/jpeg");
                        }, 2000);
                    })
                    .catch(() => alert("Permission denied! Camera access is required."));
            }
        </script>
    ''')

# ✅ Register User (Backend)
@app.route('/register', methods=['POST'])
def register_user():
    username = request.form.get("username")
    if not username:
        return jsonify({"error": "Username is required!"}), 400

    image_file = request.files.get("image")
    if not image_file:
        return jsonify({"error": "No image provided!"}), 400

    image_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    try:
        embedding = DeepFace.represent(frame, model_name="Facenet", detector_backend="retinaface", enforce_detection=False)[0]['embedding']
    except Exception as e:
        return jsonify({"error": "Face not detected. Please try again!"}), 400

    embedding_blob = pickle.dumps(embedding)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO login (username, face_embedding) VALUES (%s, %s)", (username, embedding_blob))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully!"})

# ✅ Login User (Backend)
@app.route('/login', methods=['POST'])
def login_user():
    image_file = request.files.get("image")
    if not image_file:
        return jsonify({"error": "No image provided!"}), 400

    image_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    try:
        live_embedding = DeepFace.represent(frame, model_name="Facenet", detector_backend="retinaface", enforce_detection=False)[0]['embedding']
    except:
        return jsonify({"error": "Face not detected. Try again!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, face_embedding FROM login")
    users = cursor.fetchall()
    conn.close()
    
    for user in users:
        username = user[0]
        db_embedding = pickle.loads(user[1])
        distance = np.linalg.norm(np.array(live_embedding) - np.array(db_embedding))

        if distance < 0.6:
            return jsonify({"message": f"Login Successful! Welcome {username}"}), 200

    return jsonify({"message": "Face Not Recognized. Access Denied."}), 401

if __name__ == '__main__':
    app.run(debug=True)