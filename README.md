markdown

# Webcam Face Capture & Email Tool

A simple proof-of-concept web app that captures an image from the user's webcam (with consent via browser prompt) and sends it via email. Built as an experimental project to explore webcam APIs, Flask backends, and image handling — **not a full face recognition system** (yet).

**Note**: This is a basic demo with frontend JavaScript for webcam access and a Flask backend to email the captured image. It includes ethical safeguards and is for learning purposes only.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellowgreen)](LICENSE)
[![Commits](https://img.shields.io/github/commit-activity/m/neerajsait/Face-Recognition)](https://github.com/neerajsait/Face-Recognition/commits/main)

## Why I Built This
I wanted to learn how browser webcam access works with JavaScript (getUserMedia API) and how to securely handle image data on the backend. The idea started as a simple "capture and send" experiment — like a fun proof-of-concept for remote photo sharing or a basic attendance check-in system.  

This was a quick free-time project outside my usual full-stack work (Java/Spring Boot/React). I’m planning to expand it with actual face detection/recognition later, but right now it’s focused on the capture → process → email flow. It taught me a lot about base64 encoding, MIME emails, and why consent/ethics matter with camera access.

## Key Features
- Webcam access via browser (requires user permission — no silent capture)
- Live preview on the page
- Capture button to take a photo
- Sends the captured image automatically to a configured email via Flask backend
- Uses Gmail SMTP (with app password recommended for security)

## Screenshots
*(Highly recommended — add these to make the project look real and professional! Run it locally, take screenshots, and upload to a `/screenshots` folder.)*

<!-- Example placeholders — replace with your own -->
<!-- ![Webcam Preview](screenshots/preview.png) -->
<!-- ![Capture Button](screenshots/capture.png) -->
<!-- ![Email Received](screenshots/email.png) -->

## Tech Stack
- **Frontend** — HTML + JavaScript (getUserMedia API)
- **Backend** — Python 3.8+ with Flask
- **Email** — smtplib + Gmail SMTP

## Installation & Setup
### Prerequisites
- Python 3.8+
- A Gmail account (enable 2FA and create an [App Password](https://support.google.com/accounts/answer/185833))

### Steps
1. Clone the repo
   ```bash
   git clone https://github.com/neerajsait/Face-Recognition.git
   cd Face-Recognition

(Recommended) Create a virtual environmentbash

python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

Install dependenciesbash

pip install flask

Configure email (edit app.py)Replace EMAIL_ADDRESS with your Gmail
Replace EMAIL_PASSWORD with your App Password
Replace RECIPIENT_EMAIL with the destination

Run the appbash

python app.py

Open in browser
Visit http://localhost:5000 (or your IP if testing remotely)Allow camera permission when prompted, preview yourself, and click capture to test the email.

What I Learned & ChallengesBrowser webcam access is straightforward with getUserMedia, but handling the dataURL → base64 → bytes conversion took some debugging.
Sending images via email with MIME was new to me — learned how to properly attach binary data.
Biggest challenge: making sure everything works over HTTP (HTTPS would be better for production to avoid permission issues).
Reinforced how important user consent is — the browser forces a permission prompt, which is good.

Future ImprovementsAdd actual face detection (e.g., with face-api.js or OpenCV)
Store images locally or in cloud storage instead of just email
User authentication and multiple recipients
Better UI with React
Deploy to Render/Heroku for live demo

Important Ethics & Security NoteThis tool is strictly for educational and personal testing purposes only.It requires explicit user permission to access the camera (browser will always prompt).
Never use this on others without clear consent.
Do not deploy publicly without proper security (e.g., authentication, HTTPS).
Capturing images without permission is illegal and unethical in most jurisdictions.
I am not responsible for any misuse.

Use responsibly — ideally only on your own device for learning.LicenseMIT License — see the LICENSE file for details.Built in my free time by @neerajsait while exploring web technologies. Feedback or suggestions welcome!

