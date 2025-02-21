import cv2
import numpy as np
import pickle
import mysql.connector
from flask import Flask, request, jsonify

from deepface import DeepFace

app = Flask(__name__)

# 📌 Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="password", 
        database="face_auth"
    )

# 📌 Capture Face from Webcam
def capture_face():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return None
    return frame

# 📌 Home Route (With Links to Register & Login)
@app.route('/')
def home():
    return '''
        <h1>Face Recognition API</h1>
        <p>Welcome! Use the links below to register or login.</p>
        <ul>
            <li><a href="/register">Register</a></li>
            <li><a href="/login">Login</a></li>
        </ul>
    '''

# 📌 Register Page (GET Route)
@app.route('/register', methods=['GET'])
def register_page():
    return '''
        <h2>Register</h2>
        <form action="/register" method="post">
            <label>Username:</label>
            <input type="text" name="username" required>
            <button type="submit">Register</button>
        </form>
    '''

# 📌 Login Page (GET Route)
@app.route('/login', methods=['GET'])
def login_page():
    return '''
        <h2>Login</h2>
        <form action="/login" method="post">
            <button type="submit">Login with Face</button>
        </form>
    '''

# 📌 Register User (Save Face Embeddings)
@app.route('/register', methods=['POST'])
def register_user():
    username = request.form.get('username')

    if not username:
        return jsonify({"error": "Username is required!"}), 400
    
    expressions = ["neutral", "smile", "angry"]
    face_embeddings = []

    for exp in expressions:
        print(f"Capture {exp} expression...")
        frame = capture_face()
        
        if frame is None:
            return jsonify({"error": "Face capture failed. Try again!"}), 400

        try:
            embedding = DeepFace.represent(frame, model_name="Facenet")[0]['embedding']
            face_embeddings.append(pickle.dumps(embedding))  # Convert to binary
        except:
            return jsonify({"error": "Face not detected. Try again!"}), 400

    # Store in Database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, neutral_face, smile_face, angry_face) VALUES (%s, %s, %s, %s)", 
        (username, face_embeddings[0], face_embeddings[1], face_embeddings[2])
    )
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User registered successfully!"})

# 📌 Login User (Face Recognition)
@app.route('/login', methods=['POST'])
def login_user():
    frame = capture_face()

    if frame is None:
        return jsonify({"error": "Face capture failed. Try again!"}), 400

    try:
        live_embedding = DeepFace.represent(frame, model_name="Facenet")[0]['embedding']
    except:
        return jsonify({"error": "Face not detected. Try again!"}), 400

    # Fetch stored faces
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, neutral_face, smile_face, angry_face FROM users")
    users = cursor.fetchall()
    conn.close()
    
    for user in users:
        username = user[0]
        
        for stored_face in user[1:]:
            db_embedding = pickle.loads(stored_face)
            distance = np.linalg.norm(np.array(live_embedding) - np.array(db_embedding))
            
            if distance < 0.6:  # Matching threshold
                return jsonify({"message": f"Login Successful! Welcome {username}"})
    
    return jsonify({"message": "Face Not Recognized. Access Denied."})

if __name__ == '__main__':
    app.run(debug=True)
