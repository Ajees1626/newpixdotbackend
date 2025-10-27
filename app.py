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
CORS(app)

# -----------------------------
# Gmail Config
# -----------------------------
EMAIL_ADDRESS = os.getenv("EMAIL_USER", "pixdotsolutions@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

# -----------------------------
# Root Route
# -----------------------------
@app.route("/")
def home():
    return "✅ Pixdot Backend Running (Gmail SMTP Integration Active)", 200


# -----------------------------
# Send Email Route
# -----------------------------
@app.route("/send_email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not all([name, email, message]):
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        # Email to admin
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = f"📩 New Contact Message from {name}"

        body = f"""
        You received a new message from your website contact form:

        👤 Name: {name}
        📧 Email: {email}

        💬 Message:
        {message}
        """
        msg.attach(MIMEText(body, "plain"))

        # Send email (using SSL)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("✅ Email sent successfully!")
        return jsonify({"success": True, "message": "Email sent successfully!"}), 200

    except smtplib.SMTPAuthenticationError:
        print("❌ Gmail authentication failed. Check App Password.")
        return jsonify({"success": False, "error": "Invalid Gmail credentials"}), 500

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------
# Run Flask App
# -----------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
