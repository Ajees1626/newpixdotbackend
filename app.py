from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes and domains
CORS(app, resources={r"/*": {"origins": "*"}})

# -----------------------------
# Gmail Credentials (App Password required)
# -----------------------------
EMAIL_ADDRESS = os.getenv("EMAIL_USER", "pixdotsolutions@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

# Debug log
print(f"📧 Email user loaded: {'✅' if EMAIL_ADDRESS else '❌ MISSING'}")


# -----------------------------
# Root route (for Render health check)
# -----------------------------
@app.route('/')
def home():
    return "Pixdot Backend Running 🚀 (Gmail SMTP Integration Active)"


# -----------------------------
# Send Email Route
# -----------------------------
@app.route('/send_email', methods=['POST', 'OPTIONS'])
def send_email():
    # Handle CORS preflight request
    if request.method == "OPTIONS":
        response = jsonify({"status": "OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data received'}), 400

        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not all([name, email, message]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        # Compose admin email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = f"📩 New Contact Message from {name}"

        email_body = f"""
        You have received a new message from your website contact form:

        👤 Name: {name}
        📧 Email: {email}

        💬 Message:
        {message}
        """
        msg.attach(MIMEText(email_body, 'plain'))

        # Send via Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("✅ Email sent successfully!")
        return jsonify({'success': True, 'message': 'Email sent successfully!'}), 200

    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP Authentication Failed — Check Gmail App Password!")
        return jsonify({'success': False, 'error': 'Invalid Gmail credentials'}), 500

    except Exception as e:
        print(f"❌ Server Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# -----------------------------
# Run App
# -----------------------------
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
