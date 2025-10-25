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
CORS(app)

# Gmail credentials (from .env or Render environment variables)
EMAIL_ADDRESS = os.getenv("EMAIL_USER") or os.getenv("GMAIL_USER")  # e.g. pixdotsolutions@gmail.com
EMAIL_PASSWORD = os.getenv("EMAIL_PASS") or os.getenv("GMAIL_PASS")  # App Password, not Gmail login

print(f"📧 Email User: {'✅ Set' if EMAIL_ADDRESS else '❌ Missing'}")
print(f"📧 Email Pass: {'✅ Set' if EMAIL_PASSWORD else '❌ Missing'}")

@app.route("/")
def home():
    return "Pixdot Backend Running 🚀 (Gmail SMTP)"

@app.route("/api/contact", methods=["POST", "OPTIONS"])
def contact():
    if request.method == "OPTIONS":
        response = jsonify({"status": "OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON body received"}), 400

        required = ["firstName", "lastName", "email", "subject", "message"]
        for field in required:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400

        # Email message to admin
        admin_msg = MIMEMultipart()
        admin_msg["From"] = EMAIL_ADDRESS
        admin_msg["To"] = "pixdotsolutions@gmail.com"
        admin_msg["Subject"] = f"New Contact: {data['firstName']} {data['lastName']}"

        admin_body = f"""
        📩 New Contact Form Submission

        👤 Name: {data['firstName']} {data['lastName']}
        📧 Email: {data['email']}
        📱 Phone: {data.get('phone', 'N/A')}
        🏢 Company: {data.get('company', 'N/A')}
        📝 Subject: {data['subject']}
        💬 Message:
        {data['message']}
        """
        admin_msg.attach(MIMEText(admin_body, "plain"))

        # Auto-reply to user
        user_msg = MIMEMultipart()
        user_msg["From"] = EMAIL_ADDRESS
        user_msg["To"] = data["email"]
        user_msg["Subject"] = "Thank you for contacting Pixdot Solutions"

        user_body = f"""
        Dear {data['firstName']},

        ✅ Thank you for contacting Pixdot Solutions!
        We've received your message and will get back to you within 24 hours.

        📌 Your Message:
        {data['message']}

        📞 Need urgent help? Call us at:
        • +91-87789 96278
        • +91-87789 64644

        📧 Email: info@pixdotsolutions.com

        Best regards,
        Team Pixdot Solutions 🚀
        """
        user_msg.attach(MIMEText(user_body, "plain"))

        # Send both emails via Gmail SMTP
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(admin_msg)
                server.send_message(user_msg)

            print("✅ Emails sent successfully!")
            return jsonify({
                "success": True, 
                "message": "Emails sent successfully",
                "admin_email": "pixdotsolutions@gmail.com",
                "user_email": data["email"]
            }), 200

        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Gmail Authentication Error: {e}")
            return jsonify({"error": "Gmail authentication failed. Please check your credentials."}), 500
        except smtplib.SMTPException as e:
            print(f"❌ SMTP Error: {e}")
            return jsonify({"error": f"Email sending failed: {str(e)}"}), 500

    except Exception as e:
        print(f"❌ Server Error: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
