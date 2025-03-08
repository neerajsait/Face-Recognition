# Webcam Image Capture and Email Sender

⚠️ Ethical Usage Warning:
This project is intended only for ethical and legal purposes. Any misuse, unauthorized surveillance, or violation of privacy laws is strictly prohibited. Ensure that you obtain explicit consent before capturing or processing any images. The developers are not responsible for any unethical or illegal use of this software.
## Overview
This project is a **web-based application** that captures an image from the user's webcam, sends it to a backend server using Flask, and emails the captured image to a specified recipient. It integrates **HTML, JavaScript, Flask, and SMTP** to provide a seamless user experience for image capture and email notifications.

## Features
- **Webcam Access & Image Capture**: Requests user permission to access the webcam and captures an image after a delay.
- **Automatic Image Sending**: The captured image is converted to a Base64 string and sent to the backend.
- **Email Integration**: The backend decodes the image and emails it to a predefined recipient using SMTP.
- **Error Handling**: Handles cases like denied permissions, missing camera devices, and email failures.
- **Flask API**: Provides an endpoint (`/send-image`) to handle image processing and email sending.

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **Email Service:** SMTP (Gmail)

---

## Project Structure
```
webcam_image_sender/
│-- static/
│   ├── script.js   # JavaScript for webcam access and image sending
│-- templates/
│   ├── index.html  # HTML page with webcam functionality
│-- app.py          # Flask backend for image handling and email sending
│-- requirements.txt # Dependencies for the project
│-- README.md       # Project documentation
```

---

## Setup Instructions
### Prerequisites
Ensure you have Python installed. If not, download and install it from [Python's official site](https://www.python.org/downloads/).

### 1. Clone the Repository
```sh
 git clone https://github.com/yourusername/webcam-image-sender.git
 cd webcam-image-sender
```

### 2. Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure Email Credentials
Update `app.py` with your Gmail credentials:
```python
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"
RECIPIENT_EMAIL = "recipient-email@gmail.com"
```
**Note:** Use an [App Password](https://myaccount.google.com/apppasswords) instead of your regular password.

### 5. Run the Flask Server
```sh
python app.py
```

### 6. Access the Application
Open a browser and go to:
```
http://localhost:5000/
```

---

## Usage
1. The page will request **camera access**.
2. Once access is granted, the camera will turn on briefly.
3. After 5 seconds, an image will be **captured**.
4. The image is then **sent to the server** and forwarded via **email**.
5. The camera **turns off** automatically after capturing the image.

---

## API Endpoints
| Endpoint       | Method | Description |
|---------------|--------|-------------|
| `/`           | GET    | Renders the main page |
| `/send-image` | POST   | Accepts Base64-encoded image and sends it via email |

---

## Troubleshooting
### 1. Camera Not Detected?
- Ensure your webcam is **not in use** by another application.
- Try using a **different browser**.

### 2. Email Not Sent?
- Check if you have **enabled Less Secure Apps** or used **App Passwords**.
- Ensure your **internet connection** is stable.

### 3. Flask App Not Running?
- Ensure all dependencies are installed correctly.
- Run `python app.py` in the correct directory.

---

## Future Improvements
- Add **user authentication** before capturing an image.
- Provide an option to **preview the image** before sending.
- Implement **cloud storage** integration for saving images.
- Enhance **UI/UX** for a smoother user experience.

---

## License
This project is licensed under the **MIT License**.

---

## Contributors
- **Tiruveedhi Neeraj Venkata Sai** ([@yourusername](https://github.com/yourusername))

Feel free to fork and contribute! 🚀

