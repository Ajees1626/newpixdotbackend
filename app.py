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

# Enable CORS for all domains (important for React frontend)
CORS(app, resources={r"/*": {"origins": "*"}})

# Gmail credentials (use App Password, not normal password)
EMAIL_ADDRESS = os.getenv("EMAIL_USER")  # e.g. pixdotsolutions@gmail.com
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")  # App Password

# Debug info
print(f"📧 Email User: {'✅ Set' if EMAIL_ADDRESS else '❌ Missing'}")

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return "Pixdot Backend Running 🚀 (Gmail SMTP Integration Active)"


@app.route("/api/contact", methods=["POST", "OPTIONS"])
def contact():
    # Handle CORS preflight
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

        required_fields = ["firstName", "lastName", "email", "subject", "message"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400

        # --------------------------------
        # Compose email to admin
        # --------------------------------
        admin_msg = MIMEMultipart()
        admin_msg["From"] = EMAIL_ADDRESS
        admin_msg["To"] = "pixdotsolutions@gmail.com"
        admin_msg["Subject"] = f"New Contact from {data['firstName']} {data['lastName']}"

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

        # --------------------------------
        # Compose auto-reply to user
        # --------------------------------
        user_msg = MIMEMultipart()
        user_msg["From"] = EMAIL_ADDRESS
        user_msg["To"] = data["email"]
        user_msg["Subject"] = "Thank you for contacting Pixdot Solutions"

        user_body = f"""
        Dear {data['firstName']},

        ✅ Thank you for reaching out to Pixdot Solutions!
        We’ve received your message and will get back to you within 24 hours.

        📌 Your Message:
        {data['message']}

        📞 For quick assistance, contact:
        • +91-87789 96278
        • +91-87789 64644

        📧 Email: info@pixdotsolutions.com

        Best regards,
        Team Pixdot Solutions 🚀
        """
        user_msg.attach(MIMEText(user_body, "plain"))

        # --------------------------------
        # Send both emails via Gmail SMTP
        # --------------------------------
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(admin_msg)
            server.send_message(user_msg)

        print("✅ Emails sent successfully!")
        return jsonify({"success": True, "message": "Emails sent successfully"}), 200

    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP Authentication Failed — check Gmail App Password!")
        return jsonify({"error": "Invalid email credentials"}), 500

    except Exception as e:
        print(f"❌ Server Error: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    # Get port from environment variable (Railway sets this automatically)
    port = int(os.getenv("PORT", 5000))
    # host="0.0.0.0" allows external access (Railway compatible)
    # debug=False for production deployment
    app.run(debug=False, host="0.0.0.0", port=port)
