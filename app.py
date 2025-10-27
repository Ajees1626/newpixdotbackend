from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS

# Gmail credentials
EMAIL_ADDRESS = os.getenv("EMAIL_USER", "pixdotsolutions@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

@app.route('/')
def home():
    return "Pixdot Backend Running 🚀 (Gmail SMTP Integration Active)"

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not all([name, email, message]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        # Create email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = f"New message from {name}"

        email_body = f"From: {name}\nEmail: {email}\nMessage:\n{message}"
        msg.attach(MIMEText(email_body, 'plain'))

        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({'success': True, 'message': 'Email sent successfully!'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)